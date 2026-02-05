from datetime import timedelta
import os
from django.views import View

from app.enums.responseCodes import ResponseCodes
from app.helpers.baseResponse import BaseResponse
from app.helpers.cookieHelper import CookieHelper
from app.helpers.exceptionHelper import ExceptionHelper
from app.mapping.accountMapping import AccountMapping
from app.services.accountService import AccountService
from asgiref.sync import sync_to_async


class RestockToken(View):
    async def get(self, request):
        try:
           
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token:
                result = await sync_to_async(AccountService.restock_token)(refresh_token)
                account = AccountMapping(result.get("account")).data
                return CookieHelper.attach(
                    response=BaseResponse.success(
                        data=account, 
                        code=ResponseCodes.RESTOCK_TOKEN_SUCCESS, 
                        message="Restock token successfully"
                    ), 
                    cookies={
                        "access_token": {
                            "value": result.get("access_token"),
                            "httponly": os.environ.get("COOKIE_HTTP_ONLY", True),
                            "secure": os.environ.get("COOKIE_SECURE", True),
                            "samesite": os.environ.get("COOKIE_SAMESITE", "Lax"),
                            "max_age": timedelta(days=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 15)))
                        },
                        "refresh_token": {
                            "value": result.get("refresh_token"),
                            "httponly": os.environ.get("COOKIE_HTTP_ONLY", True),
                            "secure": os.environ.get("COOKIE_SECURE", True),
                            "samesite": os.environ.get("COOKIE_SAMESITE", "Lax"),
                            "max_age": timedelta(days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", 7)))
                        }
                    }
                )
            ExceptionHelper.throw_unauthorized("Missing token")

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)