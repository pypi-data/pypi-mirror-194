from __future__ import annotations
import dataclasses
from ..shared import datefilter as shared_datefilter
from ..shared import lead as shared_lead
from ..shared import stringfilter as shared_stringfilter
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclasses.dataclass
class SearchCrmLeadsQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    cursor: Optional[str] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'cursor', 'style': 'form', 'explode': True }})
    limit: Optional[float] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'limit', 'style': 'form', 'explode': True }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class SearchCrmLeadsRequestBodyFilters:
    account: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('account'), 'exclude': lambda f: f is None }})
    created_time: Optional[shared_datefilter.DateFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('createdTime'), 'exclude': lambda f: f is None }})
    email: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('email'), 'exclude': lambda f: f is None }})
    first_name: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('firstName'), 'exclude': lambda f: f is None }})
    id: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('id'), 'exclude': lambda f: f is None }})
    job_title: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('jobTitle'), 'exclude': lambda f: f is None }})
    last_name: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('lastName'), 'exclude': lambda f: f is None }})
    mobile_phone: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('mobilePhone'), 'exclude': lambda f: f is None }})
    modified_time: Optional[shared_datefilter.DateFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('modifiedTime'), 'exclude': lambda f: f is None }})
    native_id: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('nativeId'), 'exclude': lambda f: f is None }})
    phone: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('phone'), 'exclude': lambda f: f is None }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class SearchCrmLeadsRequestBody:
    filters: Optional[SearchCrmLeadsRequestBodyFilters] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('filters'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class SearchCrmLeadsRequest:
    query_params: SearchCrmLeadsQueryParams = dataclasses.field()
    request: Optional[SearchCrmLeadsRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class SearchCrmLeadsResponseBody:
    leads: Optional[list[shared_lead.Lead]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('leads'), 'exclude': lambda f: f is None }})
    next_page_cursor: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('nextPageCursor'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class SearchCrmLeadsResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[SearchCrmLeadsResponseBody] = dataclasses.field(default=None)
    