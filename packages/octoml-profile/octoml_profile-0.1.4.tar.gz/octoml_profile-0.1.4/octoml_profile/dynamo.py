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

import atexit
import contextlib
import functools
import os
import sys
import tempfile
import threading
import time
import traceback
import warnings
import weakref
from collections import OrderedDict
from dataclasses import dataclass
from typing import (Callable, Dict, Optional, Sequence, TextIO, Tuple,
                    Union)

import numpy as np
import onnx
import torch
import torch._dynamo as torchdynamo
from torch._dynamo.backends.common import fake_tensor_unsupported
import torch._guards
import torch.fx
from torch.jit import TracerWarning

from .client import RemoteInferenceSession
from .errors import CompilationError, LoadModelError
from .inference_session import BackendSpec, InferenceSession, ModelRunner, _DefaultSession
from .log_util import LOGFILE, get_file_logger
from .workaround import _in_torch_dynamo, _onnx_export_diagnostic_patch
from .report import (PerBackendResult, Profile, ProfileReport, Segment,
                     TotalPerBackendResult, PerBackendError)

filelog = get_file_logger(__name__)


def _torchscript_to_onnx(torchscript,
                         example_inputs: Tuple[torch.Tensor, ...],
                         input_names: Sequence[str],
                         output_names: Sequence[str],
                         dirpath: str) -> str:
    model_path = os.path.join(dirpath, "model.onnx")
    torch.onnx.export(
        torchscript,
        example_inputs,
        model_path,
        input_names=input_names,
        output_names=output_names,
        opset_version=17,
        training=torch.onnx.TrainingMode.EVAL
    )

    onnx_model = onnx.load(model_path)

    external_data_dir = os.path.join(dirpath, "external")
    os.mkdir(external_data_dir)
    externalized_model_path = os.path.join(external_data_dir, "model.onnx")
    onnx.save_model(onnx_model, externalized_model_path, save_as_external_data=True,
                    all_tensors_to_one_file=True, location="external_data",
                    size_threshold=1024, convert_attribute=False)
    return external_data_dir


def _validate_onnx_input(dirpath: str,
                         input_names: Sequence[str]) -> Union[Sequence[str], Sequence[bool]]:
    model_path = os.path.join(dirpath, "model.onnx")
    onnx_model = onnx.load(model_path)
    onnx_input_names = set(inp.name for inp in onnx_model.graph.input)
    active_input_mask = tuple(n in onnx_input_names for n in input_names)
    active_input_names = tuple(n for n, is_active in zip(input_names, active_input_mask)
                               if is_active)
    return active_input_names, active_input_mask


@dataclass
class _Context:
    session: weakref.ReferenceType
    trace_recorder: '_TraceRecorder'
    last_graph_id: int

    def new_graph_id(self) -> int:
        self.last_graph_id += 1
        return self.last_graph_id

    def dec_graph_id(self):
        self.last_graph_id -= 1


@dataclass
class _GraphInfo:
    graph_id: int
    num_nodes: int
    graph_module: torch.fx.GraphModule


@dataclass
class _LocalCpuSegment:
    run_time_nanos: int

    def footprint(self):
        return None

    def add(self, sample: '_LocalCpuSegment'):
        self.run_time_nanos += sample.run_time_nanos


@dataclass
class _BackendErrors:
    count: int
    unique_errors_to_count: Dict[str, int]


@dataclass
class _CompiledSegment:
    graph: _GraphInfo
    run_times_per_backend: Dict[BackendSpec, np.ndarray]
    errors_per_backend: Dict[BackendSpec, _BackendErrors]

    def footprint(self):
        return self.graph.graph_id

    def add(self, sample: '_CompiledSegment'):
        for backend, times in sample.run_times_per_backend.items():
            self.run_times_per_backend[backend] = \
                np.concatenate((self.run_times_per_backend[backend], times))

        for backend, error in sample.errors_per_backend.items():
            agg = self.errors_per_backend[backend]
            agg.count += error.count
            for err, err_count in error.unique_errors_to_count.items():
                if err not in agg.unique_errors_to_count:
                    agg.unique_errors_to_count[err] = 0
                agg.unique_errors_to_count[err] += err_count


@dataclass
class _AggregatedResult:
    sums: Sequence[Union[_LocalCpuSegment, _CompiledSegment]]
    num_samples: int
    compilation_occurred: bool

    def add(self, sample: Sequence[Union[_LocalCpuSegment, _CompiledSegment]]):
        assert self.compilation_occurred is False, \
            "Should not aggregate to result that has compilation occurred"
        assert len(self.sums) == len(sample)
        for agg, new in zip(self.sums, sample):
            agg.add(new)
        self.num_samples += 1

    def report(self):
        segments = []
        total_uncompiled_ms = 0.0
        total_per_backend = OrderedDict()
        for segment_idx, segment in enumerate(self.sums):
            if isinstance(segment, _LocalCpuSegment):
                mean_ms = segment.run_time_nanos / 1.0e6 / self.num_samples
                total_uncompiled_ms += mean_ms
                r = PerBackendResult(mean_ms=mean_ms,
                                     num_samples=self.num_samples,
                                     num_failures=0)
                segments.append(Segment(graph_id=None,
                                        results_per_backend=OrderedDict(Uncompiled=r)))
            elif isinstance(segment, _CompiledSegment):
                results_per_backend = OrderedDict()
                for backend, run_times in segment.run_times_per_backend.items():
                    backend_str = str(backend)
                    if backend_str not in total_per_backend:
                        total_per_backend[backend_str] = TotalPerBackendResult(
                                estimated_total_ms=0.0,
                                errors=[])
                    backend_total = total_per_backend[backend_str]

                    if len(run_times) > 0:
                        mean_ms = np.mean(run_times / 1.0e6)
                        if backend_total.estimated_total_ms is not None:
                            backend_total.estimated_total_ms += mean_ms
                    else:
                        mean_ms = None
                        backend_total.estimated_total_ms = None

                    err = segment.errors_per_backend[backend]
                    if err.count > 0:
                        total_per_backend[backend_str].errors.append(PerBackendError(
                                graph_id=segment.graph.graph_id,
                                error_messages_to_count=err.unique_errors_to_count))
                    results_per_backend[backend_str] = PerBackendResult(
                            mean_ms=mean_ms,
                            num_samples=len(run_times),
                            num_failures=err.count)

                segments.append(Segment(graph_id=segment.graph.graph_id,
                                        results_per_backend=results_per_backend))
            else:
                assert False

        for backend_total in total_per_backend.values():
            if backend_total.estimated_total_ms is not None:
                backend_total.estimated_total_ms += total_uncompiled_ms

        return Profile(segments=segments,
                       total_uncompiled_ms=total_uncompiled_ms,
                       total_per_backend=total_per_backend,
                       compilation_occurred=self.compilation_occurred)


class _TraceRecorder:
    def __init__(self):
        self._start_nanos = None
        self._segments = []
        self._result_by_footprint = OrderedDict()
        self._compilation_occurred = False
        self._num_discarded_runs = 0
        self._compile_errors = []

    def start_cpu(self):
        start = time.perf_counter_ns()
        assert self._start_nanos is None
        self._start_nanos = start

    def stop_cpu(self):
        end_nanos = time.perf_counter_ns()
        assert self._start_nanos is not None
        self._segments.append(_LocalCpuSegment(end_nanos - self._start_nanos))
        self._start_nanos = None

    @contextlib.contextmanager
    def pause_cpu(self) -> Callable[[], None]:
        end_nanos = time.perf_counter_ns()
        if self._start_nanos is None:
            yield
            return
        self._segments.append(_LocalCpuSegment(end_nanos - self._start_nanos))
        self._start_nanos = None
        try:
            yield
        finally:
            self.start_cpu()

    def add_compiled_segment(self, segment: _CompiledSegment):
        assert self._start_nanos is None
        self._segments.append(segment)

    def compilation_occurred(self):
        self._compilation_occurred = True

    def add_compile_error(self, error: str):
        self._compile_errors.append(error)

    def end_run(self):
        run_footprint = tuple(s.footprint() for s in self._segments)
        agg_result = self._result_by_footprint.get(run_footprint, None)
        if self._compilation_occurred:
            assert agg_result is None
            self._result_by_footprint[run_footprint] = \
                _AggregatedResult(tuple(self._segments), 1, True)
        elif agg_result is not None:
            if agg_result.compilation_occurred:
                self._result_by_footprint[run_footprint] = \
                    _AggregatedResult(tuple(self._segments), 1, False)
            else:
                agg_result.add(self._segments)
        else:
            # got here with compilation_occurred False
            # and no agg_result means torchdynamo failed
            pass

        if self._compilation_occurred:
            self._compilation_occurred = False
            self._num_discarded_runs += 1
        self._segments.clear()

    def report(self):
        return ProfileReport(profiles=[r.report() for r in self._result_by_footprint.values()],
                             num_discarded_runs=self._num_discarded_runs,
                             compile_errors=self._compile_errors)

    def print_results(self, file=sys.stdout):
        self.report().print(file=file)


class _ThreadLocalState(threading.local):
    profiling_ctx: _Context = None


_thread_local_state = _ThreadLocalState()


def _run(runner: ModelRunner, graph_info: _GraphInfo, active_input_mask: Sequence[bool],
         *inputs: torch.Tensor):
    if _in_torch_dynamo():
        # Torchdynamo may run user compiled function during compilation, e.g.
        # for verifying correctness. This adds user overhead and also has side
        # effects to recorder. We can just pretend to run eager because remote
        # run with benchmark side effect is strongly undesirable. The flip side
        # is that `verify_correctness` is not repsected, which we do not care.
        return graph_info.graph_module(*inputs)

    recorder = _thread_local_state.profiling_ctx.trace_recorder
    with recorder.pause_cpu():
        assert len(inputs) == len(active_input_mask), "invalid number of inputs for runner"
        numpy_inputs = (x.data.cpu().numpy() for x, is_active in zip(inputs, active_input_mask)
                        if is_active)
        num_repeats = 10
        result_by_backend = runner.run(numpy_inputs, num_repeats=num_repeats)
        errors_per_backend = {}
        run_times_per_backend = {}
        for backend, r in result_by_backend.items():
            if r.error_value is None:
                err = _BackendErrors(0, {})
            else:
                err = _BackendErrors(num_repeats, {r.error_value.message: num_repeats})
                log = get_file_logger(__name__)
                log.error("Error in run graph %d for backend %s: %s",
                          graph_info.graph_id, backend, r.error_value.message)
            errors_per_backend[backend] = err

            run_times_per_backend[backend] = \
                r.result_value.run_times_nanos if r.result_value is not None else []
        recorder.add_compiled_segment(_CompiledSegment(
            graph=graph_info,
            run_times_per_backend=run_times_per_backend,
            errors_per_backend=errors_per_backend
        ))
        return graph_info.graph_module(*inputs)


# Follows torch/_dynamo/backends/onnxrt.py to disable fake tensor
@fake_tensor_unsupported
def _safe_remote_dynamo_backend(gm: torch.fx.GraphModule,
                                example_inputs: Tuple[torch.Tensor, ...]):
    try:
        return _remote_dynamo_backend(gm, example_inputs)
    except Exception as e:
        ctx = _thread_local_state.profiling_ctx
        graph_id = ctx.last_graph_id
        error = f"Graph #{graph_id} ran locally because "
        if isinstance(e, torch.onnx.errors.OnnxExporterError):
            if isinstance(e, torch.onnx.errors.UnsupportedOperatorError):
                reason = "export to onnx failed: UnsupportedOperator"
            else:
                reason = f"export to onnx failed: {type(e)}"
        elif isinstance(e, LoadModelError):
            reason = "load graph failed"
        else:
            reason = f"of {type(e)}"
        message = error + reason
        trace = traceback.format_exc()
        graph_dump = f"Graph #{graph_id} dump:\n{gm.print_readable(print_output=False)}"
        filelog.error("%s\n%s\n%s", message, graph_dump, trace)
        ctx.trace_recorder.add_compile_error(message)
    return gm.forward


def _remote_dynamo_backend(gm: torch.fx.GraphModule,
                           example_inputs: Tuple[torch.Tensor, ...]):
    recorder = _thread_local_state.profiling_ctx.trace_recorder
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', TracerWarning)
        warnings.simplefilter('ignore', UserWarning)
        recorder.compilation_occurred()

        if gm.training:
            gm.eval()

        graph_info = _GraphInfo(graph_id=_thread_local_state.profiling_ctx.new_graph_id(),
                                num_nodes=len(gm.graph.nodes),
                                graph_module=gm)

        torchscript = torch.jit.trace(gm, example_inputs)

        example_outputs = torchscript(*example_inputs)
        if isinstance(example_outputs, (tuple, list)):
            num_outputs = len(example_outputs)
        else:
            num_outputs = 1

        if num_outputs == 0:
            _thread_local_state.profiling_ctx.dec_graph_id()
            return gm.forward

        input_names = [f'input_{i}' for i in range(len(example_inputs))]
        output_names = [f'output_{i}' for i in range(num_outputs)]

        with tempfile.TemporaryDirectory() as dirpath:
            model_dirpath = _torchscript_to_onnx(torchscript, example_inputs, input_names,
                                                 output_names, dirpath)
            active_input_names, active_input_mask = _validate_onnx_input(dirpath, input_names)
            runner = _thread_local_state.profiling_ctx.session().load_onnx_model(
                model_dirpath, active_input_names, output_names)
        ret = functools.partial(_run, runner, graph_info, active_input_mask)
        return ret


class ProfileHandle:
    def __init__(self, ctx: _Context):
        self._ctx = ctx

    def report(self) -> ProfileReport:
        return self._ctx.trace_recorder.report()


def _set_profiling_ctx(ctx: Optional[_Context]):
    _thread_local_state.profiling_ctx = ctx


def _print_results_if_requested(ctx: _Context, file: Optional[TextIO]):
    if file is not None:
        ctx.trace_recorder.print_results(file=file)


@contextlib.contextmanager
def remote_profile(session: Optional[InferenceSession] = None,
                   *,
                   print_results_to: Optional[TextIO] = sys.stdout) -> ProfileHandle:
    if _thread_local_state.profiling_ctx is not None:
        raise RuntimeError("Nested remote_profile() contexts are not allowed")

    if session is None:
        if _DefaultSession.session is None:
            session = RemoteInferenceSession().as_default()
        else:
            session = InferenceSession.get_default()
    elif _DefaultSession.session is None:
        session.as_default()

    atexit.register(session.close)
    ctx = _Context(session=weakref.ref(session), trace_recorder=_TraceRecorder(), last_graph_id=0)
    del session

    with contextlib.ExitStack() as guard:
        _set_profiling_ctx(ctx)
        guard.enter_context(torch.no_grad())
        guard.enter_context(_onnx_export_diagnostic_patch())
        guard.callback(_set_profiling_ctx, None)
        guard.callback(_print_results_if_requested, ctx, print_results_to)

        # Invalidated dynamo cache because session has changed
        torchdynamo.reset()

        yield ProfileHandle(ctx)


@contextlib.contextmanager
def _profile_run():
    recorder = _thread_local_state.profiling_ctx.trace_recorder
    recorder.start_cpu()
    try:
        yield
    finally:
        recorder.stop_cpu()
        recorder.end_run()


@dataclass
class _DynamizedModuleInner:
    original_module: torch.nn.Module
    decorated_forward: Callable


class _AcceleratedModule(torch.nn.Module):
    def __init__(self, original_module: torch.nn.Module, decorated_forward):
        object.__setattr__(self, '_accelerated_module_inner', None)
        super().__init__()
        object.__setattr__(self, '_accelerated_module_inner',
                           _DynamizedModuleInner(original_module, decorated_forward))

    def __getattribute__(self, name):
        inner = object.__getattribute__(self, '_accelerated_module_inner')
        if inner is None:
            # Still in __init__
            return object.__getattribute__(self, name)
        else:
            if name == "forward":
                return inner.decorated_forward
            else:
                return getattr(inner.original_module, name)

    def __setattr__(self, key, value):
        inner = object.__getattribute__(self, '_accelerated_module_inner')
        if inner is None:
            # Still in __init__
            return object.__setattr__(self, key, value)
        else:
            return setattr(inner.original_module, key, value)


def accelerate(*args, **kwargs):
    direct_application = len(args) == 1 and len(kwargs) == 0 and callable(args[0])

    if not direct_application and len(args) > 0:
        raise ValueError('accelerate() accepts no positional arguments')

    local_backend = kwargs.get('local_backend', 'onnxrt')
    available_backends = torchdynamo.list_backends()
    if local_backend not in available_backends:
        backends_str = ','.join(available_backends)
        raise ValueError(f'Unknown backend {local_backend}. Available torch dynamo '
                         f'backends are: {backends_str}')

    regular_dynamo_decorator = torchdynamo.optimize(local_backend)
    profiling_dynamo_decorator = torchdynamo.optimize(_safe_remote_dynamo_backend)

    def decorate(func):
        if isinstance(func, torch.nn.Module):
            decorated_forward = decorate(func.forward)
            return _AcceleratedModule(func, decorated_forward)

        regular_dynamo_decorated = regular_dynamo_decorator(func)
        profiling_dynamo_decorated = profiling_dynamo_decorator(func)

        @functools.wraps(regular_dynamo_decorated)
        def decorated_func(*args, **kwargs):
            if _thread_local_state.profiling_ctx is None:
                return regular_dynamo_decorated(*args, **kwargs)

            exception = None
            with _profile_run():
                try:
                    return profiling_dynamo_decorated(*args, **kwargs)
                except torchdynamo.exc.TorchDynamoException as e:
                    exception = type(e).__name__.split(".")[-1]
                    trace = traceback.format_exc()
                except Exception as e:
                    exception = type(e).__name__
                    trace = traceback.format_exc()

            if exception:
                action = "The error above may be caused by user code error in "\
                         "the decorated function "\
                         "or a bug in TorchDynamo. In the former case, please "\
                         "check the trace for user code error; "\
                         "in the latter case, please "\
                         "try refining the scope of @accelerate closer to "\
                         "model inference."
                filelog.error("%s\n%s", trace, action)
                raise CompilationError(exception, {'details': LOGFILE})

        return decorated_func

    if direct_application:
        return decorate(args[0])
    else:
        return decorate
