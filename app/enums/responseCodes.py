from enum import Enum

class ResponseCodes(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    def __str__(self):
        return self.value