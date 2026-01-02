from rest_framework.exceptions import (
    APIException,
    ParseError,
    AuthenticationFailed,
    PermissionDenied,
    NotFound,
)

from app.enums.responseMessages import ResponseMessages

class ExceptionHelper:
    @staticmethod
    def handle_caught_exception(error: Exception, message: str = ResponseMessages.UNEXPECTED_ERROR):
        if isinstance(error, APIException):
            raise error
        if isinstance(error, Exception):
            raise APIException(str(error))
        raise APIException(message)

    @staticmethod
    def throw_bad_request(message: str = ResponseMessages.BAD_REQUEST):
        raise ParseError(message)

    @staticmethod
    def throw_not_found(message: str = ResponseMessages.NOT_FOUND):
        raise NotFound(message)

    @staticmethod
    def throw_unauthorized(message: str = ResponseMessages.UNAUTHORIZED):
        raise AuthenticationFailed(message)

    @staticmethod
    def throw_forbidden(message: str = ResponseMessages.FORBIDDEN):
        raise PermissionDenied(message)

    @staticmethod
    def throw_server_error(message: str = ResponseMessages.SERVER_ERROR):
        raise APIException(detail=message, code='server_error')