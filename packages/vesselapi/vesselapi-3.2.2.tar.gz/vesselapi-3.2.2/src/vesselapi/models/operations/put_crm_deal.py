from __future__ import annotations
import dataclasses
from ..shared import dealupdate as shared_dealupdate
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PutCrmDealRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    deal: shared_dealupdate.DealUpdate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('deal') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PutCrmDealRequest:
    request: Optional[PutCrmDealRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PutCrmDealResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PutCrmDealResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PutCrmDealResponseBody] = dataclasses.field(default=None)
    