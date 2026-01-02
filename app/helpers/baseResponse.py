from django.http import JsonResponse
from typing import Dict
from app.enums.responseCodes import ResponseCodes


class BaseResponse:
    @staticmethod
    def success(
        *,
        data: Dict | None = None,
        code: str = ResponseCodes.SUCCESS,
        message: str = "Success",
        status_code: int = 200,
    ):
        payload = {
            "success": True,
            "code": code,
            "message": message,
            "data": data,
        }

        return JsonResponse(
            payload,
            status=status_code,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def error(
        *,
        code: str,
        message: str,
        status_code: int,
        details: Dict | None = None,
    ):
        payload = {
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "details": details,
            },
        }

        return JsonResponse(
            payload,
            status=status_code,
            json_dumps_params={"ensure_ascii": False},
        )