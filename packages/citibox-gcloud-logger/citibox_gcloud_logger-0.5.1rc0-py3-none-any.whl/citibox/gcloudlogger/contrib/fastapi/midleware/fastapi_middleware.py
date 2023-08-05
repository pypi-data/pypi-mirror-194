import traceback
from typing import List, Dict, Tuple, AsyncGenerator, Awaitable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import StreamingResponse, Response
from starlette.types import ASGIApp, Message

from citibox.gcloudlogger.contrib import Middleware
from citibox.gcloudlogger.contrib.fastapi.fastapi_record_factory import FastApiRecordFactory
from citibox.gcloudlogger.src import LogException


class GcloudLoggerMiddleware(BaseHTTPMiddleware, Middleware):

    def __init__(self, app: ASGIApp) -> None:
        BaseHTTPMiddleware.__init__(self, app)
        Middleware.__init__(self)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = None
        response_content_bytes = None
        log_exception = None

        created_at = FastApiRecordFactory.get_current_timestamp()
        request_body_bytes = await request.body()

        async def _receive() -> Awaitable[Message]:
            return {'type': 'http.request', 'body': request_body_bytes, 'more_body': False}

        request_with_body = Request(request.scope, _receive)

        try:
            response = await call_next(request_with_body)
            response_content_bytes, response_headers, response_status = await self._get_response_params(response)

            async def body_stream() -> AsyncGenerator[bytes, None]:
                yield response_content_bytes

            new_response = StreamingResponse(
                status_code=response_status, content=body_stream()
            )
            new_response.raw_headers = response.raw_headers

        except Exception as exception:
            log_exception = LogException(
                exception=exception,
                traceback=traceback.format_exc()
            )
            raise exception
        finally:
            self.log_record(
                request=request,
                response=response,
                request_body=request_body_bytes,
                response_body=response_content_bytes,
                exception=log_exception,
                created_at=created_at
            )

        return new_response

    def log_record(
        self,
        request,
        response,
        request_body,
        response_body,
        exception,
        created_at
    ):
        try:
            log_record_factory = FastApiRecordFactory(
                request=request,
                response=response,
                request_body=request_body,
                response_body=response_body,
                exception=exception,
                created_at=created_at
            )
            log_record = log_record_factory.build()
            self.logger.info(
                log_record.message,
                extra=log_record.to_dict()
            )
        except Exception as e:  # pragma nocover
            pass

    async def _get_response_params(self, response) -> Tuple[bytes, Dict[str, str], int]:
        response_byte_chunks: List[bytes] = []
        response_status: List[int] = []
        response_headers: List[Dict[str, str]] = []

        async def send(message: Message) -> None:
            if message['type'] == 'http.response.start':
                response_status.append(message['status'])
                response_headers.append({k.decode('utf8'): v.decode('utf8') for k, v in message['headers']})
            else:
                response_byte_chunks.append(message['body'])

        await response.stream_response(send)
        content = b''.join(response_byte_chunks)
        return content, response_headers[0], response_status[0]
