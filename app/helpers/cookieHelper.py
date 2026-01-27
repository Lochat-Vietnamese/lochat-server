from django.http import HttpResponse
from typing import Dict

from app.types.cookieOptions import CookieOptions

class CookieHelper:
    @staticmethod
    def attach(response: HttpResponse, cookies: Dict[str, CookieOptions]) -> HttpResponse:
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
