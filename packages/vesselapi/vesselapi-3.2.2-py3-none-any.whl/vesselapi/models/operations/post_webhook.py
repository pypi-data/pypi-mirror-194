from __future__ import annotations
import dataclasses
from ..shared import webhookmetadata as shared_webhookmetadata
from ..shared import webhookmetadatacreate as shared_webhookmetadatacreate
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostWebhookRequestBody:
    access_token: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken'), 'exclude': lambda f: f is None }})
    webhook: Optional[shared_webhookmetadatacreate.WebhookMetadataCreate] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('webhook'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class PostWebhookRequest:
    request: Optional[PostWebhookRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostWebhookResponseBody:
    webhook: Optional[shared_webhookmetadata.WebhookMetadata] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('webhook'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class PostWebhookResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PostWebhookResponseBody] = dataclasses.field(default=None)
    