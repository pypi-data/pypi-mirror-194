from __future__ import annotations
import dataclasses
from ..shared import connection as shared_connection
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class GetAllCrmConnectionsResponseBody:
    connections: Optional[list[shared_connection.Connection]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('connections'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class GetAllCrmConnectionsResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetAllCrmConnectionsResponseBody] = dataclasses.field(default=None)
    