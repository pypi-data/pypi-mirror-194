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

import sys
from dataclasses import dataclass
from typing import Dict, Sequence, OrderedDict, Optional, List

from .log_util import LOGFILE


__all__ = ['PerBackendResult', 'Segment', 'TotalPerBackendResult', 'Profile', 'ProfileReport']


@dataclass
class PerBackendResult:
    mean_ms: Optional[float]
    num_samples: int
    num_failures: int


@dataclass
class Segment:
    graph_id: Optional[int]  # None if segment is uncompiled
    results_per_backend: OrderedDict[str, PerBackendResult]


@dataclass
class PerBackendError:
    graph_id: int
    error_messages_to_count: Dict[str, int]


@dataclass
class TotalPerBackendResult:
    estimated_total_ms: Optional[float]
    errors: List[PerBackendError]


@dataclass
class Profile:
    segments: Sequence[Segment]
    total_uncompiled_ms: float
    total_per_backend: OrderedDict[str, TotalPerBackendResult]
    compilation_occurred: bool

    def print(self, *, file=sys.stdout):
        self._print_segments(file)
        self._print_totals(file)
        self._print_errors(file)

    def _print_segments(self, file):
        table = [
            ("", "Segment", "Runs", "Mean ms", "Failures"),
            "="
        ]
        for segment_idx, segment in enumerate(self.segments):
            if segment.graph_id is None:
                if self.compilation_occurred:
                    continue
                r = segment.results_per_backend["Uncompiled"]
                table.append((segment_idx, "Uncompiled", r.num_samples, f"{r.mean_ms:.3f}"))
            else:
                table.append('')
                table.append((segment_idx, f"Graph #{segment.graph_id}",))
                for backend, result in segment.results_per_backend.items():
                    mean_ms = "N/A" if result.mean_ms is None else f"{result.mean_ms:.3f}"
                    table.append(("", "  " + backend,
                                  result.num_samples, mean_ms, result.num_failures))
                table.append('')
        table.append('-')
        _print_table(table, "><>>>", file)

    def _print_totals(self, file):
        if self.compilation_occurred:
            print(f'Total times (compiled + uncompiled) is not available '
                  f'because compilation has occurred.', file=file)
            print(f'Please run the function multiple times to get total '
                  f'times.', file=file)
            return
        else:
            print(f'Total uncompiled code run time: {self.total_uncompiled_ms:.3f} ms', file=file)
            print(f'Total times (compiled + uncompiled) per backend, ms:', file=file)
        table = []
        for backend, total_res in self.total_per_backend.items():
            if total_res.estimated_total_ms is None:
                estimated_total_ms = "N/A"
            else:
                estimated_total_ms = f"{total_res.estimated_total_ms:.3f}"
            table.append(("  ", backend, estimated_total_ms))
        table.append('')
        _print_table(table, "<<>", file)

    def _print_errors(self, file):
        if any([total.errors for total in self.total_per_backend.values()]):
            print('Errors occurred running this model, per backend:', file=file)
            for backend, total_res in self.total_per_backend.items():
                if not total_res.errors:
                    continue
                print(f'    {backend}', file=file)
                for error in total_res.errors:
                    graph_str = f'       Graph #{error.graph_id} - '
                    print(graph_str, end='', file=file)
                    for i, (error, count) in enumerate(error.error_messages_to_count.items()):
                        if i > 0:
                            print('\n', ' ' * (len(graph_str) - 1), end='', file=file)
                        print(f'{count} errors: {error}', end='', file=file)
                    print(file=file)
            print(f'For full client-side error traces see {LOGFILE}', file=file)


@dataclass
class ProfileReport:
    profiles: List[Profile]
    num_discarded_runs: int
    compile_errors: List[str]

    def print(self, *, file=sys.stdout):
        print(f'Runs discarded because compilation occurred: {self.num_discarded_runs}', file=file)
        if len(self.profiles) == 0:
            print('Profiling was enabled but no results were recorded', file=file)
        for i, profile in enumerate(self.profiles):
            print(f'Profile {i + 1}/{len(self.profiles)}:', file=file)
            profile.print(file=file)
        for e in self.compile_errors:
            print("WARNING: " + e, file=file)
        if len(self.compile_errors) > 0:
            print(f"See full client-side trace at {LOGFILE}")


def _string_width(s):
    # FIXME: use wcwidth if we need to display non-latin characters
    return len(str(s))


_align = {
    '<': lambda s, width: s + ' ' * max(0, width - _string_width(s)),
    '>': lambda s, width: ' ' * max(0, width - _string_width(s)) + s
}


def _print_table(rows, column_alignment: str, file):
    col_spacing = 2
    col_spacing_str = ' ' * col_spacing
    num_cols = len(column_alignment)
    column_alignment = tuple(_align[a] for a in column_alignment)

    col_width = [0] * num_cols
    for row in rows:
        if not isinstance(row, str):
            for i, cell in enumerate(row):
                col_width[i] = max(col_width[i], _string_width(cell))

    total_width = sum(col_width) + col_spacing * (num_cols - 1)
    for row in rows:
        if isinstance(row, str):
            num_reps = 1 if _string_width(row) == 0 else total_width // _string_width(row)
            print(row * num_reps, file=file)
        else:
            print(*(align(str(cell), width)
                    for cell, width, align in zip(row, col_width, column_alignment)),
                  file=file,
                  sep=col_spacing_str)
