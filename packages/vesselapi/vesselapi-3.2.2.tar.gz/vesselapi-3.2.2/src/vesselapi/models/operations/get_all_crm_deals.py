from __future__ import annotations
import dataclasses
from ..shared import deal as shared_deal
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclasses.dataclass
class GetAllCrmDealsQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    cursor: Optional[str] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'cursor', 'style': 'form', 'explode': True }})
    limit: Optional[float] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'limit', 'style': 'form', 'explode': True }})
    

@dataclasses.dataclass
class GetAllCrmDealsRequest:
    query_params: GetAllCrmDealsQueryParams = dataclasses.field()
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class GetAllCrmDealsResponseBody:
    deals: Optional[list[shared_deal.Deal]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('deals'), 'exclude': lambda f: f is None }})
    next_page_cursor: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('nextPageCursor'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class GetAllCrmDealsResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetAllCrmDealsResponseBody] = dataclasses.field(default=None)
    