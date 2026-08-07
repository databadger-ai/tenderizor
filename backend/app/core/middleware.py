from collections.abc import Awaitable, Callable
from time import perf_counter
from uuid import UUID, uuid4

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import get_logger

logger = get_logger("http")


def _uuid_header(value: str | None) -> str:
    if value is None:
        return str(uuid4())
    try:
        return str(UUID(value))
    except ValueError:
        return str(uuid4())


class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        correlation_id = _uuid_header(request.headers.get("x-correlation-id"))
        request_id = _uuid_header(request.headers.get("x-request-id"))
        request.state.correlation_id = correlation_id
        request.state.request_id = request_id
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            service=request.app.state.settings.service_name,
            component="http",
            correlation_id=correlation_id,
            request_id=request_id,
            tender_id=None,
            workflow_id=None,
            status="STARTED",
            error_class=None,
        )
        started = perf_counter()
        try:
            try:
                response = await call_next(request)
            except Exception as exc:
                logger.exception(
                    "request_failed",
                    method=request.method,
                    path=request.url.path,
                    status="FAILED",
                    error_class=type(exc).__name__,
                    latency_ms=round((perf_counter() - started) * 1000, 2),
                )
                raise

            response.headers["X-Correlation-ID"] = correlation_id
            response.headers["X-Request-ID"] = request_id
            logger.info(
                "request_completed",
                method=request.method,
                path=request.url.path,
                http_status=response.status_code,
                status="SUCCEEDED" if response.status_code < 500 else "FAILED",
                latency_ms=round((perf_counter() - started) * 1000, 2),
            )
            return response
        finally:
            structlog.contextvars.clear_contextvars()
