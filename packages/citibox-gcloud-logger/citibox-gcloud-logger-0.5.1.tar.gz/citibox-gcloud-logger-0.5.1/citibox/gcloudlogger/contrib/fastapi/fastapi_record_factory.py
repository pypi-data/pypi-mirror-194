import json
from logging import getLogger
from typing import Optional

from citibox.gcloudlogger.src.base_record import Params, RequestHeaders, Body, ResponseHeaders, UserInfo
from citibox.gcloudlogger.src.base_record_factory import BaseLogRecordFactory
from citibox.gcloudlogger.src import LogException

logger = getLogger(__name__)


class FastApiRecordFactory(BaseLogRecordFactory):

    JSON_TYPE = 'application/json'
    OCTET_STREAM_TYPE = 'application/octet-stream'

    def __init__(
        self,
        request,
        response,
        request_body,
        response_body,
        exception: LogException = None,
        created_at=None
    ):
        self.request = request
        self.response = response
        self.request_body = request_body
        self.response_body = response_body
        self.exception = exception

        super().__init__(created_at=created_at)

    def _build_request_params(self) -> Params:
        return Params(**self.request.query_params)

    @classmethod
    def _parse_body(cls, content_type, body) -> Body:
        if content_type == cls.JSON_TYPE:
            return Body(**json.loads(body.decode()))
        elif content_type == cls.OCTET_STREAM_TYPE:
            return body

    def _build_request_body(self) -> Body:
        if self.request_body:
            return self._parse_body(self.request.headers.get('content-type'), self.request_body)

        return Body()

    def _build_request_headers(self) -> RequestHeaders:
        return RequestHeaders(
            **{header: value if header.lower() != 'authorization' else '****' for header, value in self.request.headers.items()}
        )

    def _get_user_info(self) -> Optional[UserInfo]:
        header = self.request.headers.get(self.USER_INFO_HEADER)
        return UserInfo(header) if header else None

    def _build_response_headers(self) -> ResponseHeaders:
        if self.response:
            return ResponseHeaders(**self.response.headers)

        return ResponseHeaders()

    def _build_response_body(self) -> Body:
        if self.response_body:
            return self._parse_body(self.response.headers.get('content-type'), self.response_body)

        return Body()

    def _build_pubsub_request_attributes(self) -> dict:
        if self.request.headers.get('user-agent', '').upper() == self.PUBSUB_USER_AGENT.upper():
            data = self._parse_body(self.JSON_TYPE, self.request_body).to_dict()
            return data['message']['attributes']

        return dict()

    def _get_request_uri_path(self) -> str:
        return self.request.scope.get('path')

    def _get_url_fingerprint(self) -> str:
        return self.request.scope.get('route').path

    def _get_request_view_params(self) -> dict:
        return self.request.path_params

    def _get_host(self) -> str:
        return self.request.headers.get('host', self.request.base_url)

    def _get_method(self) -> str:
        return self.request.method

    def _get_status_code(self) -> int:
        if self.response:
            return self.response.status_code

        return 500
