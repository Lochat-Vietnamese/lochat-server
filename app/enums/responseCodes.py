from enum import Enum

class ResponseCodes(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    SIGN_UP_SUCCESS = "SIGN_UP_SUCCESS"
    RESTOCK_TOKEN_SUCCESS = "RESTOCK_TOKEN_SUCCESS"
    LOGOUT_SUCCESS = "LOGOUT_SUCCESS"
    GET_ACCOUNT_BY_ID_SUCCESS = "GET_ACCOUNT_BY_ID_SUCCESS"

    def __str__(self):
        return self.value