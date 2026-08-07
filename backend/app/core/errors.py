from http import HTTPStatus


class AppError(Exception):
    status_code = HTTPStatus.BAD_REQUEST
    code = "application_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(AppError):
    status_code = HTTPStatus.NOT_FOUND
    code = "not_found"


class ConflictError(AppError):
    status_code = HTTPStatus.CONFLICT
    code = "conflict"


class DependencyUnavailableError(AppError):
    status_code = HTTPStatus.SERVICE_UNAVAILABLE
    code = "dependency_unavailable"


class PayloadTooLargeError(AppError):
    status_code = HTTPStatus.REQUEST_ENTITY_TOO_LARGE
    code = "payload_too_large"


class ImmutableAuditError(RuntimeError):
    """Raised when code attempts to mutate or delete an audit event."""
