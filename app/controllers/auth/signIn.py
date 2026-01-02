from datetime import timedelta
import os
from django.views import View

from app.dtos.authDTOs import SignInDTO
from app.mapping.accountMapping import AccountMapping
from app.services.accountService import AccountService
from app.utils.baseResponse import BaseResponse
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData


class SignInController(View):
    async def post(self, request):
        try:
            raw_data = RequestData(request=request)
            sign_in_dto = SignInDTO(**raw_data)

            result = await AccountService.login(sign_in_dto)
            account = AccountMapping(result.get("account")).data
            
            return BaseResponse.send(data=account, cookies=self._set_cookies(result))
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