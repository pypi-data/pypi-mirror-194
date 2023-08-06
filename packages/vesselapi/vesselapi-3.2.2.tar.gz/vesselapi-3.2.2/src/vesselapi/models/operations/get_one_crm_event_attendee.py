from __future__ import annotations
import dataclasses
from ..shared import eventattendee as shared_eventattendee
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclasses.dataclass
class GetOneCrmEventAttendeeQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    id: str = dataclasses.field(metadata={'query_param': { 'field_name': 'id', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    

@dataclasses.dataclass
class GetOneCrmEventAttendeeRequest:
    query_params: GetOneCrmEventAttendeeQueryParams = dataclasses.field()
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class GetOneCrmEventAttendeeResponseBody:
    event_attendee: Optional[shared_eventattendee.EventAttendee] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('eventAttendee'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class GetOneCrmEventAttendeeResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetOneCrmEventAttendeeResponseBody] = dataclasses.field(default=None)
    