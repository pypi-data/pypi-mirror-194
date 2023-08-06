from __future__ import annotations
import dataclasses
from ..shared import integration as shared_integration
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class GetAllCrmIntegrationsResponseBody:
    integrations: Optional[list[shared_integration.Integration]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('integrations'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class GetAllCrmIntegrationsResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetAllCrmIntegrationsResponseBody] = dataclasses.field(default=None)
    