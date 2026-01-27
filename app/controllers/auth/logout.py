import os
from django.views import View

from app.enums.responseCodes import ResponseCodes
from app.helpers.baseResponse import BaseResponse
from app.helpers.cookieHelper import CookieHelper
from app.helpers.exceptionHelper import ExceptionHelper
from app.services.accountService import AccountService


class Logout(View):
    async def get(self, request):
        try:
           
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token:
                await AccountService.logout(refresh_token)

            return CookieHelper.attach(
                response=BaseResponse.success(
                    code=ResponseCodes.LOGOUT_SUCCESS, 
                    message="Logout successfully"
                ), 
                cookies={
                    "access_token": {
                        "value": "",
                        "httponly": os.environ.get("COOKIE_HTTP_ONLY", True),
                        "secure": os.environ.get("COOKIE_SECURE", True),
                        "samesite": os.environ.get("COOKIE_SAMESITE", "Lax"),
                        "max_age": 0
                    },
                    "refresh_token": {
                        "value": "",
                        "httponly": os.environ.get("COOKIE_HTTP_ONLY", True),
                        "secure": os.environ.get("COOKIE_SECURE", True),
                        "samesite": os.environ.get("COOKIE_SAMESITE", "Lax"),
                        "max_age": 0
                    }
                }
            )

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)