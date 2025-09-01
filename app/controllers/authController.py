from rest_framework.views import APIView
from app.services.accountService import AccountService
from app.mapping.accountMapping import AccountMapping
from app.utils.dictHelper import DictHelper
from app.utils.baseResponse import BaseResponse


class AuthController(APIView):
    async def post(self, request, action=None):
        try:
            if action == "login":
                username = request.data.get("username")
                email = request.data.get("email")
                password = request.data.get("password")

                if (username or email) and password:
                    result = await AccountService.login(request.data)
                    if result:
                        result["account"] = AccountMapping(result.get("account")).data
                        return BaseResponse.success(data=result)
                    return BaseResponse.error("login_failed")
                return BaseResponse.error(message="invalid_data")

            if action and action == "sign_up":
                username = request.data.get("username")
                email = request.data.get("email")
                password = request.data.get("password")
                nickname = request.data.get("nickname")
                dob = request.data.get("dob")
                phone_number = request.data.get("phone_number")

                if all([username, nickname, email, password, dob, phone_number]):
                    result = await AccountService.sign_up(
                        DictHelper.parse_python_dict(AccountMapping(data=request.data))
                    )
                    if result:
                        return BaseResponse.success(data=AccountMapping(result).data)
                    return BaseResponse.error(message="sign_up_failed")
                return BaseResponse.error(message="invalid_data")

            if action and action == "restock-token":
                token = request.data.get("token")
                if token:
                    result = await AccountService.restock_token(token)
                    if result:
                        result["account"] = AccountMapping(result.get("account")).data
                        return BaseResponse.success(data=result)
                    return BaseResponse.error("restock_failed")
                return BaseResponse.error(message="invalid_data")

            return BaseResponse.error(message="invalid_endpoint")
        except Exception as e:
            return BaseResponse.internal(data=str(e))
