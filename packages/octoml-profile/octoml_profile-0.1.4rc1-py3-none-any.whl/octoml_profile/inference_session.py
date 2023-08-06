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

import numpy as np
import threading
import weakref
from dataclasses import dataclass
from typing import Sequence, Mapping, NamedTuple, Tuple
from .protos import remote_inference_pb2 as pb
from .conversion_util import proto_to_numpy


class BackendSpec(NamedTuple):
    hardware_platform: str
    software_backend: str

    @staticmethod
    def parse(spec: str) -> 'BackendSpec':
        hw_and_sw = spec.split('/', maxsplit=1)
        if len(hw_and_sw) != 2:
            raise ValueError('Backend spec string must contain a hardware platform name'
                             ' and a software backend name, separated by a slash,'
                             ' e.g. "aws-v100/onnxrt-cuda"')
        hardware_platform, software_backend = hw_and_sw
        return BackendSpec(hardware_platform, software_backend)

    def __str__(self):
        return f"{self.hardware_platform}/{self.software_backend}"

    def __format__(self, format_spec):
        return format(str(self), format_spec)


@dataclass
class ResultValue:
    outputs: Tuple[np.ndarray, ...]
    run_times_nanos: np.ndarray  # 1D array of int64


@dataclass
class RunResult:
    result_value: ResultValue
    error_value: str

    @staticmethod
    def from_pb(result: pb.RunResult) -> "RunResult":
        result_value, error_value = None, None
        if result.HasField("result_value"):
            result_value = ResultValue(
                outputs=tuple(proto_to_numpy(x) for x in result.result_value.outputs),
                run_times_nanos=np.array(result.result_value.run_times_nanos, dtype=np.int64)
            )
        else:
            error_value = result.error_value
        return RunResult(result_value, error_value)


class ModelRunner:
    def run(self, inputs, num_repeats=None) -> Mapping[BackendSpec, RunResult]:
        raise NotImplementedError


class _DefaultSession(threading.local):
    session = None  # optional weakref to InferenceSession


class InferenceSession:
    def __init__(self):
        self._previous_default_session = None
        self._set_as_default = False

    @staticmethod
    def get_default() -> "InferenceSession":
        ret = _DefaultSession.session() if _DefaultSession.session is not None else None
        if ret is None:
            raise ValueError('No default RemoteInferenceSession is currently set')
        return ret

    def as_default(self) -> "InferenceSession":
        self._previous_default_session = _DefaultSession.session
        _DefaultSession.session = weakref.ref(self)
        self._set_as_default = True
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._set_as_default:
            _DefaultSession.session = self._previous_default_session
            self._previous_default_session = None
            self._set_as_default = False
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        raise NotImplementedError

    def load_onnx_model(self,
                        path: str,
                        input_names: Sequence[str],
                        output_names: Sequence[str]) -> ModelRunner:
        raise NotImplementedError
