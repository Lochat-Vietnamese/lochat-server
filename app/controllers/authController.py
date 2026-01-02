from datetime import timedelta
import os
from django.views import View

from app.dtos.authDTOs import SignInDTO, SignUpDTO
from app.enums.responseMessages import ResponseMessages
from app.services.accountService import AccountService
from app.mapping.accountMapping import AccountMapping
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData


class AuthController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)

            if action == "login":
                sign_in_dto = SignInDTO(**data)

                result = await AccountService.login(sign_in_dto)
                account = AccountMapping(result.get("account")).data
               
                return BaseResponse.send(data=account, cookies={
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
                })

            if action == "sign-up":
                sign_up_dto = SignUpDTO(**data)

                result = await AccountService.sign_up(sign_up_dto)
                return BaseResponse.send(data=AccountMapping(result).data)

            if action == "restock-token":
                refresh_token = request.COOKIES.get("refresh_token")

                if refresh_token:
                    result = await AccountService.restock_token(refresh_token)
                    account = AccountMapping(result.get("account")).data
                    return BaseResponse.send(data=account, cookies={
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
                    })
                ExceptionHelper.throw_unauthorized(ResponseMessages.MISSING_TOKEN)
                
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_ENDPOINT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
