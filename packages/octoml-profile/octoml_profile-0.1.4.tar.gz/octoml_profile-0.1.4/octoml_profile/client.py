# Copyright 2023 OctoML, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import os
import sys
import threading
import weakref
from contextlib import ExitStack
from typing import Iterator, List, Mapping, Optional, Sequence, Tuple, Union
from uuid import UUID

import grpc

from .interceptors.auth import AuthInterceptor, StreamAuthInterceptor
from .interceptors.cookie import CookieInterceptor, StreamCookieInterceptor
from .errors import LoadModelError, CreateSessionError
from .protos import remote_inference_pb2 as pb, remote_inference_pb2_grpc as rpc
from .conversion_util import numpy_to_proto, proto_to_backend_str

from .inference_session import (BackendSpec, InferenceSession, ModelRunner,
                                RunResult)
from .log_util import LOGFILE, get_file_logger


BackendSpecType = Union[str, BackendSpec, Sequence[Union[str, BackendSpec,
                                                         pb.BackendSpec]]]


MAX_GRPC_MESSAGE_SIZE = 1024 * 1024 * 1024   # 1GiB


class RemoteModelRunner(ModelRunner):
    def __init__(self,
                 session: 'RemoteInferenceSession',
                 model_id: int):
        self._session = weakref.ref(session)
        self._model_id = model_id

    def run(self, inputs, num_repeats=None) -> Mapping[BackendSpec, RunResult]:
        session = self._session()
        input_protos = [numpy_to_proto(x) for x in inputs]
        request = pb.RunRequest(session_uuid=session._session_uuid.bytes,
                                model_id=self._model_id,
                                inputs=input_protos,
                                num_repeats=num_repeats)
        reply = session._stub.Run(request)
        assert len(reply.result_per_backend) == len(session._backends)
        return {
            backend: RunResult.from_pb(result)
            for backend, result in zip(session._backends, reply.result_per_backend)
        }


def _get_backend_specs(backends: Optional[BackendSpecType] = None)\
        -> Sequence[BackendSpec]:
    if backends is None:
        return []
    if isinstance(backends, str):
        return BackendSpec.parse(backends),
    elif isinstance(backends, BackendSpec):
        return backends
    else:
        ret = []
        for backend in backends:
            if isinstance(backend, str):
                ret.append(BackendSpec.parse(backend))
            elif isinstance(backend, BackendSpec):
                ret.append(backend)
            elif isinstance(backend, pb.BackendSpec):
                ret.append(BackendSpec(backend.hardware_platform, backend.software_backend))
            else:
                raise TypeError(f'Expected a string or a BackendSpec, got {type(backend)}')
        return ret


def _heartbeat_thread(stub: rpc.RemoteInferenceStub,
                      session_uuid: UUID,
                      quit_event: threading.Event):
    HEARTBEAT_PERIOD_SECONDS = 10
    RETRY_TIMEOUT_SECONDS = 1

    next_timeout = HEARTBEAT_PERIOD_SECONDS
    prev_future = None

    while True:
        if quit_event.wait(timeout=next_timeout):
            break

        if prev_future is not None:
            if not prev_future.done():
                next_timeout = RETRY_TIMEOUT_SECONDS
                continue

        try:
            prev_future = stub.Heartbeat.future(
                pb.HeartbeatRequest(session_uuid=session_uuid.bytes))
        except grpc.RpcError:
            # TODO: log?
            next_timeout = RETRY_TIMEOUT_SECONDS
            prev_future = None
            continue

        next_timeout = HEARTBEAT_PERIOD_SECONDS


def _sha256_file(path: str) -> bytes:
    hash = hashlib.sha256()
    with open(path, "rb", buffering=0) as f:
        buf = bytearray(64 * 1024)
        view = memoryview(buf)
        while True:
            bytes_read = f.readinto(view)
            if bytes_read == 0:
                break
            hash.update(view[:bytes_read])
    return hash.digest()


class RemoteInferenceSession(InferenceSession):
    def __init__(self,
                 backends: Optional[BackendSpecType] = None,
                 server_addr: str = 'dynamite.prod.aws.octoml.ai',
                 insecure: bool = False,
                 access_token: Optional[str] = None):
        super().__init__()
        self._supported_backends = None
        self._channel = None
        self._stub = None
        self._session_uuid = None
        self._next_model_id = 1
        self._heartbeat_thread = None
        self._heartbeat_quit_event = threading.Event()
        self._logger = get_file_logger(__name__)
        self._backends = _get_backend_specs(backends)
        backend_protos = [
            pb.BackendSpec(hardware_platform=b.hardware_platform,
                           software_backend=b.software_backend) for b in self._backends
        ]
        access_token = os.environ.get("OCTOML_PROFILE_API_TOKEN", None) or access_token
        server_addr = os.environ.get("OCTOML_PROFILE_ENDPOINT", None) or server_addr

        with ExitStack() as guard:
            if insecure:
                self._channel = grpc.insecure_channel(
                    server_addr,
                    options=(
                        ('grpc.max_send_message_length', MAX_GRPC_MESSAGE_SIZE),
                        ('grpc.max_receive_message_length', MAX_GRPC_MESSAGE_SIZE),
                    ),
                )
            else:
                credentials = grpc.ssl_channel_credentials()
                self._channel = grpc.secure_channel(
                    server_addr,
                    credentials,
                    options=(
                        ('grpc.max_send_message_length', MAX_GRPC_MESSAGE_SIZE),
                        ('grpc.max_receive_message_length', MAX_GRPC_MESSAGE_SIZE),
                    ),
                )
                if access_token is not None:
                    self._channel = grpc.intercept_channel(self._channel,
                                                           AuthInterceptor(access_token),
                                                           StreamAuthInterceptor(access_token))

            def reset_channel():
                self._channel.close()
                # Set _channel to None so that __del__ doesn't try to send any messages over it
                # or to close it again
                self._channel = None

            guard.callback(reset_channel)

            self._stub = rpc.RemoteInferenceStub(self._channel)

            try:
                # Before creating the session, check that requested backends are valid
                self._supported_backends = self.get_supported_backends()
                if len(backend_protos) == 0:
                    backend_protos = self._get_default_supported_backends()
                    self._backends = _get_backend_specs(backend_protos)
                    requested_backends = list(map(proto_to_backend_str, backend_protos))
                    print('No backends were requested, so '
                          f'requesting default backends {requested_backends}')
                if any([b not in self._supported_backends for b in backend_protos]):
                    requested_backends = list(map(proto_to_backend_str, backend_protos))
                    print(f'Requested {requested_backends}.')
                    self.print_supported_backends()
                    sys.exit(1)

                request = pb.CreateSessionRequest(backends=backend_protos)
                reply, call = self._stub.CreateSession.with_call(request)

                # Set cookie for sticky sessions
                for item in call.initial_metadata():
                    if item.key == 'set-cookie':
                        cookie = item.value
                        self._channel = grpc.intercept_channel(self._channel,
                                                               CookieInterceptor(cookie),
                                                               StreamCookieInterceptor(cookie))
                        self._stub = rpc.RemoteInferenceStub(self._channel)

                if reply.WhichOneof('result') == 'error_value':
                    error_value = reply.error_value
                    if error_value.code == pb.ERROR_BACKEND_NONEXISTENT:
                        requested_backends = list(map(proto_to_backend_str, backend_protos))
                        print(f'Requested {requested_backends}.')
                        self.print_supported_backends()
                        sys.exit(1)
                    else:
                        print(error_value.message)
                        sys.exit(1)

            except grpc.RpcError as rpc_error:
                # Extract the details of the gRPC error
                if hasattr(rpc_error, "debug_error_string"):
                    status_debug_string = f" [debug_error_string: {rpc_error.debug_error_string()}]"
                else:
                    status_debug_string = ""

                self._logger.error("An error occurred in CreateSession RPC:"
                                   f" {status_debug_string}", exc_info=True)

                # TODO(yuanjing_octoml): handle more status code types
                status_code = rpc_error.code()
                status_details = rpc_error.details()
                if status_code == grpc.StatusCode.UNAVAILABLE:
                    status_details = "Connection can't be established between client and server. " \
                                     "This could be caused by incorrect ip addresses or port " \
                                     "numbers"
                elif status_code == grpc.StatusCode.INTERNAL:
                    status_details = "An internal error ocurred, typically due to starting " \
                                     "the remote session with wrong configuration(s)"

                # use from None to suppress stack trace from rpc_error
                raise CreateSessionError(f"Error {status_code.name}:"
                                         f" {status_details}. See full client-side"
                                         f" trace at {LOGFILE}") from None

            reply = reply.result_value
            self._session_uuid = UUID(bytes=reply.session_uuid)
            self._logger.info(f"Created session with uuid {self._session_uuid}")

            # If we get a KeyboardInterrupt or another exception before returning from __init__,
            # we want to attempt to send a CloseSession() request if possible.
            # This is most likely to happen when the user gives up on waiting for the session
            # to start and hits Ctrl-C.
            guard.callback(self._send_close_session_message_silently)

            if not reply.ready:
                print('Waiting for an available remote worker...', file=sys.stderr)
                while True:
                    reply = self._stub.WaitUntilSessionReady(
                        pb.WaitUntilSessionReadyRequest(session_uuid=self._session_uuid.bytes))

                    if reply.ready:
                        print('Acquired all workers, session is now ready.', file=sys.stderr)
                        break

            guard.pop_all()

        self._heartbeat_thread = threading.Thread(
            target=_heartbeat_thread,
            kwargs=dict(
                stub=self._stub,
                session_uuid=self._session_uuid,
                quit_event=self._heartbeat_quit_event
            ),
            daemon=True
        )
        self._heartbeat_thread.start()

    def _send_close_session_message_silently(self):
        try:
            self._stub.CloseSession(
                pb.CloseSessionRequest(session_uuid=self._session_uuid.bytes))
        except grpc.RpcError:
            # We've done our part. In the worst case, the session
            # will time out on the server.
            pass

    def get_supported_backends(self) -> List[pb.BackendSpec]:
        if self._supported_backends is None:
            reply = self._stub.ListSupportedBackends(pb.ListSupportedBackendsRequest())
            self._supported_backends = reply.backends
        return self._supported_backends

    def _get_default_supported_backends(self) -> List[pb.BackendSpec]:
        # Get the first "onnxrt-cpu"-only platform and first "onnxrt-cuda"-included platform
        hardware_to_software = {}
        for b in self.get_supported_backends():
            if b.hardware_platform not in hardware_to_software:
                hardware_to_software[b.hardware_platform] = []
            hardware_to_software[b.hardware_platform].append(b.software_backend)

        defaults = []
        cpu_backend = None
        gpu_backend = None
        for h, ss in hardware_to_software.items():
            if len(ss) == 1 and ss[0] == "onnxrt-cpu" and cpu_backend is None:
                cpu_backend = pb.BackendSpec(hardware_platform=h, software_backend=ss[0])
                defaults.append(cpu_backend)
            elif "onnxrt-cuda" in ss and gpu_backend is None:
                gpu_backend = pb.BackendSpec(hardware_platform=h, software_backend="onnxrt-cuda")
                defaults.append(gpu_backend)

        if not defaults:
            self.print_supported_backends()
            sys.exit(1)
        return defaults

    def print_supported_backends(self):
        allowed_backend_strs = list(map(proto_to_backend_str, self.get_supported_backends()))
        allowed_backends_rep = '\n\t'.join(allowed_backend_strs)
        message = (f'The supported, valid backends are:\n\t{allowed_backends_rep}\n'
                   'Please create your remote inference session with valid backends;\n'
                   f'e.g. session = RemoteInferenceSession(["{allowed_backend_strs[0]}"])')
        print(message)

    def close(self):
        if self._heartbeat_thread is not None:
            self._heartbeat_quit_event.set()
            self._heartbeat_thread = None

        if self._channel is not None:
            if self._session_uuid is not None and self._stub is not None:
                self._send_close_session_message_silently()
                self._session_uuid = None
                self._stub = None

            self._channel.close()
            self._channel = None

    def load_onnx_model(self,
                        dirpath: str,
                        input_names: Sequence[str],
                        output_names: Sequence[str]) -> RemoteModelRunner:
        model_id = self._next_model_id
        self._next_model_id += 1

        files = os.listdir(dirpath)
        for model_component_id, filename in enumerate(files, 1):
            path = os.path.join(dirpath, filename)
            sha256 = _sha256_file(path)
            req = pb.LoadCachedModelComponentRequest(session_uuid=self._session_uuid.bytes,
                                                     model_id=model_id,
                                                     model_component_id=model_component_id,
                                                     sha256_hash=sha256,
                                                     filename=filename)

            try:
                reply = self._stub.LoadCachedModelComponent(req)
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.NOT_FOUND:
                    request_iter = _request_stream_from_file(path, self._session_uuid, model_id,
                                                             model_component_id, len(files),
                                                             filename)
                    reply = self._stub.LoadModelComponent(request_iter)
                else:
                    raise LoadModelError("Error in load cached component: "
                                         "graph {}, component {}, {}"
                                         .format(model_id, model_component_id, str(e)))

            all_errors, error_messages = self._load_error_info(model_id,
                                                               model_component_id,
                                                               self._backends,
                                                               reply.result_per_backend)

            if all_errors:
                raise LoadModelError("Error in load component: "
                                     "graph {}, component {}, {}"
                                     .format(model_id, model_component_id,
                                             str(error_messages)))

        req = pb.LoadModelRequest(session_uuid=self._session_uuid.bytes,
                                  model_id=model_id,
                                  model_format=pb.MODEL_FORMAT_ONNX,
                                  input_names=input_names,
                                  output_names=output_names)
        reply = self._stub.LoadModel(req)

        all_errors, error_messages = self._load_error_info(model_id,
                                                           None,  # component id
                                                           self._backends,
                                                           reply.result_per_backend)

        if all_errors:
            raise LoadModelError(f"Error in load graph: graph {model_id}, {str(error_messages)}")

        return RemoteModelRunner(self, model_id)

    def _load_error_info(
        self,
        model_id: int,
        model_component_id: Optional[int],
        backends: Sequence[BackendSpec],
        result_per_backend: Union[Sequence[pb.LoadModelComponentResult],
                                  Sequence[pb.LoadModelResult]]) \
            -> Tuple[bool, Sequence[str]]:
        all_errors = True
        error_messages = []
        for backend, result in zip(backends, result_per_backend):
            if result.HasField("error_value"):
                if model_component_id is None:
                    self._logger.error("Error in load graph %d on backend %s: %s",
                                       model_id, str(backend), result.error_value.message)
                else:
                    self._logger.error("Error in load graph %d "
                                       "component %d on "
                                       "backend %s: %s",
                                       model_id, model_component_id,
                                       str(backend), result.error_value.message)
                error_messages.append(result.error_value.message)
            else:
                all_errors = False
        return all_errors, error_messages


def _request_stream_from_file(path: str,
                              session_uuid: UUID,
                              model_id: int,
                              model_component_id: int,
                              num_model_components: int,
                              filename: str) -> Iterator[pb.LoadModelComponentRequest]:
    req = pb.LoadModelComponentRequest(session_uuid=session_uuid.bytes,
                                       model_id=model_id,
                                       model_component_id=model_component_id,
                                       filename=filename)
    interactive_progress = hasattr(sys.stderr, "fileno") and os.isatty(sys.stderr.fileno())
    MAX_CHUNK_LEN = 1024 * 1024
    num_chunks = 0
    with open(path, "rb") as f:
        f.seek(0, 2)
        total_size = f.tell()
        total_size_mb = total_size / (1024 * 1024)
        upload_message = "Uploading %f MB [item %d / %d of graph %d]" % (total_size_mb,
                                                                         model_component_id,
                                                                         num_model_components,
                                                                         model_id)
        if not interactive_progress:
            print(f"{upload_message}...", file=sys.stderr)
        f.seek(0, 0)
        while True:
            req.chunk = f.read(MAX_CHUNK_LEN)
            if len(req.chunk) == 0 and num_chunks > 0:
                break
            yield req
            percent_done = int(100 * f.tell() / total_size)
            if interactive_progress:
                print(f"{upload_message}... {percent_done}%\r", flush=True,
                      end='', file=sys.stderr)
            req = pb.LoadModelComponentRequest()
            num_chunks += 1
    if interactive_progress:
        print(f"{upload_message}... 100%", file=sys.stderr)
