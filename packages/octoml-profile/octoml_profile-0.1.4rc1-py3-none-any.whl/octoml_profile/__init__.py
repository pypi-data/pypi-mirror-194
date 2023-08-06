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

from . import report
from ._about import version
from .client import RemoteInferenceSession
from .dynamo import accelerate, remote_profile, ProfileHandle
from .inference_session import InferenceSession

__all__ = ["RemoteInferenceSession", "InferenceSession",
           "accelerate", "remote_profile", "report", "ProfileHandle"]

try:
    from .private import _LocalInferenceSession  # noqa: F401
    __all__.append('_LocalInferenceSession')
except ImportError:
    pass

__version__ = version
