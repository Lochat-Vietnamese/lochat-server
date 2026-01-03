from enum import Enum

class ResponseCodes(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    SIGN_UP_SUCCESS = "SIGN_UP_SUCCESS"
    RESTOCK_TOKEN_SUCCESS = "RESTOCK_TOKEN_SUCCESS"

    def __str__(self):
        return self.value