from rest_framework.exceptions import APIException
from django.utils.deprecation import MiddlewareMixin
from app.helpers.baseResponse import BaseResponse

class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, APIException):
            status_code = exception.status_code
            detail = exception.detail

            if isinstance(detail, dict):
                if 'detail' in detail:
                    message = detail['detail']
                else:
                    message = detail
            else:
                message = str(detail)            
            return BaseResponse.send(status_code=status_code, message=message)
        return None