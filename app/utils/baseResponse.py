from django.http import JsonResponse

from app.enums.responseMessages import ResponseMessages

class BaseResponse:
    @staticmethod
    def send(status_code=200, message= ResponseMessages.SUCCESS, data=None):
        return JsonResponse({
            "message": message,
            "data": data
        }, status=status_code, json_dumps_params={'ensure_ascii': False})