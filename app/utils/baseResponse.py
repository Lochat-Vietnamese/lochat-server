from django.http import JsonResponse

class BaseResponse:
    @staticmethod
    def success(status_code=200, message="success", data=None):
        return JsonResponse({
            "message": message,
            "data": data
        }, status=status_code, json_dumps_params={'ensure_ascii': False})

    @staticmethod
    def error(status_code=400, message="error", data=None):
        return JsonResponse({
            "message": message,
            "data": data
        }, status=status_code, json_dumps_params={'ensure_ascii': False})

    @staticmethod
    def not_found(status_code=404, message="not_found", data=None):
        return JsonResponse({
            "message": message,
            "data": data
        }, status=status_code, json_dumps_params={'ensure_ascii': False})

    @staticmethod
    def internal(status_code=500, message="internal_error", data=None):
        return JsonResponse({
            "message": message,
            "data": data
        }, status=status_code, json_dumps_params={'ensure_ascii': False})

    @staticmethod
    def custom(status_code: int, message: str, data=None):
        return JsonResponse({
            "message": message,
            "data": data
        }, status=status_code, json_dumps_params={'ensure_ascii': False})
