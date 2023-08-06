from __future__ import annotations
import dataclasses
from ..shared import eventattendee as shared_eventattendee
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclasses.dataclass
class GetAllCrmEventAttendeesQueryParams:
    access_token: Optional[str] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    cursor: Optional[str] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'cursor', 'style': 'form', 'explode': True }})
    limit: Optional[float] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'limit', 'style': 'form', 'explode': True }})
    

@dataclasses.dataclass
class GetAllCrmEventAttendeesRequest:
    query_params: GetAllCrmEventAttendeesQueryParams = dataclasses.field()
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class GetAllCrmEventAttendeesResponseBody:
    event_attendees: Optional[list[shared_eventattendee.EventAttendee]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('eventAttendees'), 'exclude': lambda f: f is None }})
    next_page_cursor: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('nextPageCursor'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class GetAllCrmEventAttendeesResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetAllCrmEventAttendeesResponseBody] = dataclasses.field(default=None)
    