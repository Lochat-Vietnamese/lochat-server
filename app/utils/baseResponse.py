from django.http import JsonResponse

from app.enums.responseMessages import ResponseMessages


class BaseResponse:
    @staticmethod
    def send(
        status_code=200,
        message=ResponseMessages.SUCCESS,
        data=None,
        cookies: dict | None = None,
    ):
        response = JsonResponse(
            {"message": message, "data": data},
            status=status_code,
            json_dumps_params={"ensure_ascii": False},
        )

        if cookies:
            for key, options in cookies.items():
                response.set_cookie(
                    key=key,
                    value=options["value"],
                    httponly=options.get("httponly", True),
                    secure=options.get("secure", True),
                    samesite=options.get("samesite", "Lax"),
                    max_age=options.get("max_age"),
                    path=options.get("path", "/"),
                )

        return response