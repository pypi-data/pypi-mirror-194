import requests
from . import utils
from typing import Optional
from vesselapi.models import operations

class Passthrough:
    _client: requests.Session
    _security_client: requests.Session
    _server_url: str
    _language: str
    _sdk_version: str
    _gen_version: str

    def __init__(self, client: requests.Session, security_client: requests.Session, server_url: str, language: str, sdk_version: str, gen_version: str) -> None:
        self._client = client
        self._security_client = security_client
        self._server_url = server_url
        self._language = language
        self._sdk_version = sdk_version
        self._gen_version = gen_version

    
    def create(self, request: operations.PostCrmPassthroughRequest) -> operations.PostCrmPassthroughResponse:
        r"""Passthrough Request
        Send an authenticated passthrough request to the downstream CRM. This is useful for making requests to endpoints that are not yet supported by Vessel.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix("/") + "/crm/passthrough"
        
        headers = {}
        req_content_type, data, form = utils.serialize_request_body(request)
        if req_content_type != "multipart/form-data" and req_content_type != "multipart/mixed":
            headers["content-type"] = req_content_type
        
        client = self._security_client
        
        r = client.request("POST", url, data=data, files=form, headers=headers)
        content_type = r.headers.get("Content-Type")

        res = operations.PostCrmPassthroughResponse(status_code=r.status_code, content_type=content_type)
        
        if r.status_code == 200:
            if utils.match_content_type(content_type, "application/json"):
                out = utils.unmarshal_json(r.text, Optional[operations.PostCrmPassthroughResponseBody])
                res.response_body = out

        return res

    