from django.http import JsonResponse
from typing import Dict, List
from app.enums.httpStatus import HttpStatus
from app.enums.responseCodes import ResponseCodes


class BaseResponse:
    @staticmethod
    def success(
        *,
        status_code: int = HttpStatus.OK,
        code: str = ResponseCodes.SUCCESS,
        message: str = "Success",
        data: Dict | List | None = None,
        page: int | None = None,
        page_size: int | None = None,
        total_items: int | None = None,
    ):
        total_pages = (total_items + page_size - 1) // page_size

        meta = {
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "total_items": total_items,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        }

        payload = {
            "code": code,
            "message": message,
            "data": data,
            "meta": meta
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
            "code": code,
            "message": message,
            "errors": details,
        }

        return JsonResponse(
            payload,
            status=status_code,
            json_dumps_params={"ensure_ascii": False},
        )