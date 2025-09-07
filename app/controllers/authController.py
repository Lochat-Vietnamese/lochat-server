from django.views import View

from app.services.accountService import AccountService
from app.mapping.accountMapping import AccountMapping
from app.utils.baseResponse import BaseResponse
from app.utils.logHelper import LogHelper
from app.utils.requestData import RequestData

class AuthController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)


            if action == "login":
                username = data.get("username")
                email = data.get("email")
                password = data.get("password")

                LogHelper.error("ok")

                if (username or email) and password:
                    result = await AccountService.login(data)
                    if result:
                        result["account"] = AccountMapping(result.get("account")).data
                        return BaseResponse.success(data=result)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()

            if action == "sign-up":
                username = data.get("username")
                email = data.get("email")
                password = data.get("password")
                nickname = data.get("nickname")
                dob = data.get("dob")
                phone_number = data.get("phone_number")

                if all([username, nickname, email, password, dob, phone_number]):
                    result = await AccountService.sign_up(data)
                    if result:
                        return BaseResponse.success(data=AccountMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()

            if action == "restock-token":
                token = data.get("token")
                if token:
                    result = await AccountService.restock_token(token)
                    if result:
                        result["account"] = AccountMapping(result.get("account")).data
                        return BaseResponse.success(data=result)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()
                

            return BaseResponse.error(message="invalid_endpoint")
        except Exception as e:
            return BaseResponse.internal(data=str(e))
