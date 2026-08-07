import logging
import sys
from collections.abc import MutableMapping
from typing import Any, cast

import structlog

from app.core.config import Settings

REQUIRED_LOG_FIELDS = (
    "timestamp",
    "severity",
    "service",
    "component",
    "correlation_id",
    "tender_id",
    "workflow_id",
    "request_id",
    "status",
    "error_class",
)


def _required_fields(
    _: Any, __: str, event_dict: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    event_dict["severity"] = str(event_dict.pop("level", "INFO")).upper()
    for field in REQUIRED_LOG_FIELDS:
        event_dict.setdefault(field, None)
    return event_dict


def configure_logging(settings: Settings) -> None:
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(stream=sys.stdout, format="%(message)s", level=level, force=True)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            _required_fields,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(service=settings.service_name)


def get_logger(component: str) -> structlog.stdlib.BoundLogger:
    # Supplying initial values keeps the proxy lazy. Calling ``.bind()`` here
    # would materialize module-level loggers before ``configure_logging`` runs.
    return cast(structlog.stdlib.BoundLogger, structlog.get_logger(component=component))
