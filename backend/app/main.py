from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import Settings, get_settings
from app.core.errors import AppError
from app.core.logging import configure_logging, get_logger
from app.core.middleware import CorrelationMiddleware
from app.db.session import Database
from app.services.dispatcher import (
    AnalysisDispatcher,
    FakeAnalysisDispatcher,
    TemporalAnalysisDispatcher,
)

logger = get_logger("errors")


def _request_id(request: Request) -> str:
    return str(getattr(request.state, "request_id", "unknown"))


def create_app(
    *,
    settings: Settings | None = None,
    database: Database | None = None,
    dispatcher: AnalysisDispatcher | None = None,
) -> FastAPI:
    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings)
    resolved_database = database or Database(resolved_settings.database_url)
    resolved_dispatcher = dispatcher
    if resolved_dispatcher is None:
        resolved_dispatcher = (
            FakeAnalysisDispatcher(resolved_database)
            if resolved_settings.dispatch_mode == "fake"
            else TemporalAnalysisDispatcher(resolved_settings)
        )

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        application.state.settings = resolved_settings
        application.state.database = resolved_database
        application.state.dispatcher = resolved_dispatcher
        yield
        await resolved_dispatcher.close()
        await resolved_database.dispose()

    application = FastAPI(
        title="CanadaBuys AI Tender Assistant API",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.state.settings = resolved_settings
    application.state.database = resolved_database
    application.state.dispatcher = resolved_dispatcher
    application.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "X-Actor-ID", "X-Correlation-ID", "X-Request-ID"],
    )
    application.add_middleware(CorrelationMiddleware)
    application.include_router(router)

    @application.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=int(exc.status_code),
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "request_id": _request_id(request),
                }
            },
        )

    @application.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        details = [
            {"type": item["type"], "loc": list(item["loc"]), "message": item["msg"]}
            for item in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "request validation failed",
                    "request_id": _request_id(request),
                    "details": details,
                }
            },
        )

    @application.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "unhandled_error",
            status="FAILED",
            error_class=type(exc).__name__,
            request_id=_request_id(request),
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "internal_error",
                    "message": "an unexpected error occurred",
                    "request_id": _request_id(request),
                }
            },
        )

    return application


app = create_app()
