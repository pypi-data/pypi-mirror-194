from __future__ import annotations
import dataclasses
from ..shared import accountcreate as shared_accountcreate
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmAccountRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    account: shared_accountcreate.AccountCreate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('account') }})
    

@dataclasses.dataclass
class PostCrmAccountRequest:
    request: Optional[PostCrmAccountRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmAccountResponseBody:
    id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('id'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class PostCrmAccountResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PostCrmAccountResponseBody] = dataclasses.field(default=None)
    