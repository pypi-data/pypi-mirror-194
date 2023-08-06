from __future__ import annotations
import dataclasses
from ..shared import security as shared_security
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclasses.dataclass
class PostLinkTokenSecurity:
    vessel_api_token: shared_security.SchemeVesselAPIToken = dataclasses.field(metadata={'security': { 'scheme': True, 'type': 'apiKey', 'sub_type': 'header' }})
    

@dataclasses.dataclass
class PostLinkTokenRequest:
    security: PostLinkTokenSecurity = dataclasses.field()
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostLinkTokenResponseBody:
    link_token: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('linkToken'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class PostLinkTokenResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PostLinkTokenResponseBody] = dataclasses.field(default=None)
    