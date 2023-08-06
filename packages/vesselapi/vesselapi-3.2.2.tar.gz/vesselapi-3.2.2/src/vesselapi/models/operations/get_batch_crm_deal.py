from __future__ import annotations
import dataclasses
from ..shared import deal as shared_deal
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclasses.dataclass
class GetBatchCrmDealQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    ids: Optional[str] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'ids', 'style': 'form', 'explode': True }})
    

@dataclasses.dataclass
class GetBatchCrmDealRequest:
    query_params: GetBatchCrmDealQueryParams = dataclasses.field()
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class GetBatchCrmDealResponseBody:
    deals: Optional[list[shared_deal.Deal]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('deals'), 'exclude': lambda f: f is None }})
    invalid_ids: Optional[list[str]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('invalidIds'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class GetBatchCrmDealResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetBatchCrmDealResponseBody] = dataclasses.field(default=None)
    