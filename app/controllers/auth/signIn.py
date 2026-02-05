from datetime import timedelta
import os
from django.views import View

from app.dtos.authDTOs import SignInDTO
from app.enums.responseCodes import ResponseCodes
from app.helpers.cookieHelper import CookieHelper
from app.mapping.accountMapping import AccountMapping
from app.services.accountService import AccountService
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData
from asgiref.sync import sync_to_async


class SignIn(View):
    async def post(self, request):
        try:
            raw_data = RequestData(request=request)
            sign_in_dto = SignInDTO(**raw_data)

            result = await sync_to_async(AccountService.login)(sign_in_dto.model_dump())
            account = AccountMapping(result.get("account")).data

            return CookieHelper.attach(
                response=BaseResponse.success(
                    data=account, 
                    code=ResponseCodes.LOGIN_SUCCESS, 
                    message="Login successfully"
                ), 
                cookies=self._set_cookies(result)
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
    
    def _set_cookies(self, result):
        return {
            "access_token": {
                "value": result["access_token"],
                "httponly": os.environ.get("COOKIE_HTTP_ONLY", True),
                "secure": os.environ.get("COOKIE_SECURE", True),
                "samesite": os.environ.get("COOKIE_SAMESITE", "Lax"),
                "max_age": timedelta(days=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 15))),
            },
            "refresh_token": {
                "value": result["refresh_token"],
                "httponly": os.environ.get("COOKIE_HTTP_ONLY", True),
                "secure": os.environ.get("COOKIE_SECURE", True),
                "samesite": os.environ.get("COOKIE_SAMESITE", "Lax"),
                "max_age": timedelta(days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", 7))),
            },
        }