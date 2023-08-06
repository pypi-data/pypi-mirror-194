from __future__ import annotations
import dataclasses
from ..shared import taskcreate as shared_taskcreate
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmTaskRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    task: Optional[shared_taskcreate.TaskCreate] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('task'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class PostCrmTaskRequest:
    request: Optional[PostCrmTaskRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmTaskResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PostCrmTaskResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PostCrmTaskResponseBody] = dataclasses.field(default=None)
    