# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from datetime import timezone

import aorta
import pydantic

from ..deviceinfo import DeviceInfo
from ..deviceinspector import DeviceInspector


class DeviceGraded(aorta.Event):
    id: int
    graded: datetime = pydantic.Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    grading: str
    device: DeviceInfo
    source: DeviceInspector