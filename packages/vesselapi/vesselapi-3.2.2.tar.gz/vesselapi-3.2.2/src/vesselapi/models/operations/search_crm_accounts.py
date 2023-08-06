from __future__ import annotations
import dataclasses
from ..shared import account as shared_account
from ..shared import datefilter as shared_datefilter
from ..shared import numberfilter as shared_numberfilter
from ..shared import stringfilter as shared_stringfilter
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclasses.dataclass
class SearchCrmAccountsQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    cursor: Optional[str] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'cursor', 'style': 'form', 'explode': True }})
    limit: Optional[float] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'limit', 'style': 'form', 'explode': True }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class SearchCrmAccountsRequestBodyFilters:
    annual_revenue: Optional[shared_numberfilter.NumberFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('annualRevenue'), 'exclude': lambda f: f is None }})
    city: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('city'), 'exclude': lambda f: f is None }})
    country: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('country'), 'exclude': lambda f: f is None }})
    created_time: Optional[shared_datefilter.DateFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('createdTime'), 'exclude': lambda f: f is None }})
    description: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('description'), 'exclude': lambda f: f is None }})
    id: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('id'), 'exclude': lambda f: f is None }})
    industry: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('industry'), 'exclude': lambda f: f is None }})
    modified_time: Optional[shared_datefilter.DateFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('modifiedTime'), 'exclude': lambda f: f is None }})
    name: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('name'), 'exclude': lambda f: f is None }})
    native_id: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('nativeId'), 'exclude': lambda f: f is None }})
    number_of_employees: Optional[shared_numberfilter.NumberFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('numberOfEmployees'), 'exclude': lambda f: f is None }})
    phone: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('phone'), 'exclude': lambda f: f is None }})
    postal_code: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('postalCode'), 'exclude': lambda f: f is None }})
    state: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('state'), 'exclude': lambda f: f is None }})
    street: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('street'), 'exclude': lambda f: f is None }})
    website: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('website'), 'exclude': lambda f: f is None }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class SearchCrmAccountsRequestBody:
    filters: Optional[SearchCrmAccountsRequestBodyFilters] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('filters'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class SearchCrmAccountsRequest:
    query_params: SearchCrmAccountsQueryParams = dataclasses.field()
    request: Optional[SearchCrmAccountsRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class SearchCrmAccountsResponseBody:
    accounts: Optional[list[shared_account.Account]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('accounts'), 'exclude': lambda f: f is None }})
    next_page_cursor: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('nextPageCursor'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class SearchCrmAccountsResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[SearchCrmAccountsResponseBody] = dataclasses.field(default=None)
    