from __future__ import annotations
import dataclasses
from ..shared import datefilter as shared_datefilter
from ..shared import eventattendee as shared_eventattendee
from ..shared import stringfilter as shared_stringfilter
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclasses.dataclass
class SearchCrmEventAttendeesQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    cursor: Optional[str] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'cursor', 'style': 'form', 'explode': True }})
    limit: Optional[float] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'limit', 'style': 'form', 'explode': True }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class SearchCrmEventAttendeesRequestBodyFilters:
    associated_object_type: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('associatedObjectType'), 'exclude': lambda f: f is None }})
    created_time: Optional[shared_datefilter.DateFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('createdTime'), 'exclude': lambda f: f is None }})
    email: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('email'), 'exclude': lambda f: f is None }})
    id: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('id'), 'exclude': lambda f: f is None }})
    modified_time: Optional[shared_datefilter.DateFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('modifiedTime'), 'exclude': lambda f: f is None }})
    native_id: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('nativeId'), 'exclude': lambda f: f is None }})
    status: Optional[shared_stringfilter.StringFilter] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('status'), 'exclude': lambda f: f is None }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class SearchCrmEventAttendeesRequestBody:
    filters: Optional[SearchCrmEventAttendeesRequestBodyFilters] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('filters'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class SearchCrmEventAttendeesRequest:
    query_params: SearchCrmEventAttendeesQueryParams = dataclasses.field()
    request: Optional[SearchCrmEventAttendeesRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class SearchCrmEventAttendeesResponseBody:
    event_attendees: Optional[list[shared_eventattendee.EventAttendee]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('eventAttendees'), 'exclude': lambda f: f is None }})
    next_page_cursor: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('nextPageCursor'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class SearchCrmEventAttendeesResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[SearchCrmEventAttendeesResponseBody] = dataclasses.field(default=None)
    