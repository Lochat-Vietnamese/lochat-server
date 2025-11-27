from enum import Enum

class ResponseMessages(str, Enum):
    UNEXPECTED_ERROR = "unexpected_error"
    BAD_REQUEST = "bad_request"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    SERVER_ERROR = "server_error"
    SUCCESS = "success"