from rest_framework.exceptions import (
    APIException,
    ParseError,
    AuthenticationFailed,
    PermissionDenied,
    NotFound,
    ValidationError,
    Throttled,
)

from app.types.conflictException import ConflictException

class ExceptionHelper:
    @staticmethod
    def handle_caught_exception(
        error: Exception,
        message: str = "Unexpected error",
    ):
        if isinstance(error, APIException):
            raise error

        raise APIException(detail=str(error) or message)

    @staticmethod
    def throw_bad_request(message: str = "Bad request"):
        raise ParseError(detail=message)

    @staticmethod
    def throw_validation_error(message: str | dict):
        raise ValidationError(detail=message)

    @staticmethod
    def throw_not_found(message: str = "Not found"):
        raise NotFound(detail=message)

    @staticmethod
    def throw_unauthorized(message: str = "Unauthorized"):
        raise AuthenticationFailed(detail=message)

    @staticmethod
    def throw_forbidden(message: str = "Forbidden"):
        raise PermissionDenied(detail=message)

    @staticmethod
    def throw_throttled(message: str = "Too many requests"):
        raise Throttled(detail=message)

    @staticmethod
    def throw_conflict(message: str = "Conflict"):
        raise ConflictException(detail=message)

    @staticmethod
    def throw_server_error(message: str = "Internal server error"):
        raise APIException(detail=message)
