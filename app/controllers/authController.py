from django.views import View

from app.enums.responseMessages import ResponseMessages
from app.services.accountService import AccountService
from app.mapping.accountMapping import AccountMapping
from app.utils.baseResponse import BaseResponse
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData


class AuthController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)

            if action == "login":
                username = data.get("username")
                email = data.get("email")
                password = data.get("password")

                if (username or email) and password:
                    result = await AccountService.login(data)
                    result["account"] = AccountMapping(result.get("account")).data
                    return BaseResponse.send(data=result)
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            if action == "sign-up":
                username = data.get("username")
                email = data.get("email")
                password = data.get("password")
                nickname = data.get("nickname")
                dob = data.get("dob")
                phone_number = data.get("phone_number")

                if all([username, nickname, email, password, dob, phone_number]):
                    result = await AccountService.sign_up(data)
                    return BaseResponse.send(data=AccountMapping(result).data)
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            if action == "restock-token":
                token = data.get("token")
                if token:
                    result = await AccountService.restock_token(token)
                    result["account"] = AccountMapping(result.get("account")).data
                    return BaseResponse.send(data=result)
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)
                
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_ENDPOINT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
