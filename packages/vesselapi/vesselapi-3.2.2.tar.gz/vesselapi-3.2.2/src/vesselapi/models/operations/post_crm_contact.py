from __future__ import annotations
import dataclasses
from ..shared import contactcreate as shared_contactcreate
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmContactRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    contact: shared_contactcreate.ContactCreate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('contact') }})
    

@dataclasses.dataclass
class PostCrmContactRequest:
    request: Optional[PostCrmContactRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmContactResponseBody:
    id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('id'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class PostCrmContactResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PostCrmContactResponseBody] = dataclasses.field(default=None)
    