from __future__ import annotations
import dataclasses
from ..shared import connection as shared_connection
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclasses.dataclass
class GetOneConnectionQueryParams:
    connection_id: str = dataclasses.field(metadata={'query_param': { 'field_name': 'connectionId', 'style': 'form', 'explode': True }})
    

@dataclasses.dataclass
class GetOneConnectionRequest:
    query_params: GetOneConnectionQueryParams = dataclasses.field()
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class GetOneConnectionResponseBody:
    connection: Optional[shared_connection.Connection] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('connection'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class GetOneConnectionResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetOneConnectionResponseBody] = dataclasses.field(default=None)
    