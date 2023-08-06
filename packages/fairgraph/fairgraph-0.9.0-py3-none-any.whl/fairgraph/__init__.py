"""
Python client for the EBRAINS Knowledge Graph

Authors: Andrew Davison et al., CNRS (see authors.rst)


Copyright 2018-2023 CNRS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re
from .client_v3 import KGv3Client as KGClient

__version__ = "0.9.0"

from . import (
    analysis, base_v2, base_v3, brainsimulation, client_v2, client_v3, commons, core, data,
    experiment, electrophysiology, errors, minds, optophysiology, software, uniminds, utility,
    livepapers, openminds)
