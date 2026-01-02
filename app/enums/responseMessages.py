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
    INVALID_INPUT = "invalid_inputs"
    ALREADY_EXISTS = "already_exists"
    INVALID_CREDENTIALS = "invalid_credentials"
    INVALID_TOKEN = "invalid_token"
    EXPIRED_TOKEN = "expired_token"
    MISSING_TOKEN = "missing_token"
    ACCOUNT_INACTIVE = "account_inactive"
    FILE_TOO_LARGE = "file_too_large"

    def __str__(self):
        return self.value