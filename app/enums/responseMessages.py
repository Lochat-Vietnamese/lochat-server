from enum import Enum

class ResponseMessages(str, Enum):
    UNEXPECTED_ERROR = "unexpected_error"
    BAD_REQUEST = "bad_request"
    NOT_FOUND = "data_not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    SERVER_ERROR = "server_error"
    SUCCESS = "success"
    INVALID_ENDPOINT = "invalid_endpoint"
    MISSING_DATA = "missing_data"