from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from typing import Any, Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class EventAssociations:
    account_ids: list[str] = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accountIds') }})
    contact_ids: list[str] = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('contactIds') }})
    deal_ids: list[str] = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('dealIds') }})
    event_attendee_ids: list[str] = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('eventAttendeeIds') }})
    lead_ids: list[str] = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('leadIds') }})
    owner_user_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('ownerUserId') }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class Event:
    r"""Event
    Events are a type of activity that has attendees and takes place at a certain point in time (i.e., has a start and end date).
    For the currently supported CRMs, these are the objects Events most closely maps to:
    - Salesforce = Events
    - HubSpot = Meetings
    - Pipedrive = Activities
    """
    
    associations: EventAssociations = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('associations') }})
    created_time: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('createdTime') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    modified_time: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('modifiedTime') }})
    native_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('nativeId') }})
    additional: Optional[dict[str, Any]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('additional'), 'exclude': lambda f: f is None }})
    description: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('description'), 'exclude': lambda f: f is None }})
    end_date_time: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('endDateTime'), 'exclude': lambda f: f is None }})
    is_all_day_event: Optional[bool] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('isAllDayEvent'), 'exclude': lambda f: f is None }})
    location: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('location'), 'exclude': lambda f: f is None }})
    start_date_time: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('startDateTime'), 'exclude': lambda f: f is None }})
    subject: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('subject'), 'exclude': lambda f: f is None }})
    type: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('type'), 'exclude': lambda f: f is None }})
    