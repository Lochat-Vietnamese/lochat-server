from rest_framework.views import APIView
from rest_framework import status
from app.services.accountsService import AccountsService
from app.mapping.accountMapping import AccountsMapping
from app.utils.baseResponse import BaseResponse
from app.utils.dictHelper import DictHelper
import logging

log = logging.getLogger(__name__)

class AuthController(APIView):

    def post(self, request, action = None):
        try:
            if action == "login":                
                username = str(request.data.get("username"))
                email = str(request.data.get("email"))
                password = str(request.data.get("password"))
                if (username or email) and password:
                    result = AccountsService.login(request.data)
                    if result:
                        account = result.get("account")
                        if account:
                            if not account.is_active:
                                result["account"] = None
                                return BaseResponse.success(message="deactivated", data=result)
                            result["account"] = AccountsMapping(result.get("account")).data
                            return BaseResponse.success(data=result)
                    return BaseResponse.custom(status.HTTP_401_UNAUTHORIZED, "Sai tài khoản hoặc mật khẩu")
                return BaseResponse.error(message= "Thiếu thông tin đăng nhập")
            
            if action == "validate-token":
                account_id = str(request.user_id)
                if account_id:
                    result = AccountsService.validate_token(account_id=account_id)
                    if result:
                        account = result.get("account")
                        if account:
                            if not account.is_active:
                                result["account"] = None
                                return BaseResponse.success(message="deactivated", data=result)
                            result["account"] = AccountsMapping(result.get("account")).data
                            return BaseResponse.success(data=result)
                    return BaseResponse.custom(status.HTTP_401_UNAUTHORIZED, "token không hợp lệ")
                return BaseResponse.error(message="Thiếu token")
            
            if action and action == "registry":
                username = request.data.get("username")
                nickname = request.data.get("nickname")
                email = request.data.get("email")
                password = request.data.get("password")
                birth = request.data.get("birth")

                if all([username, nickname, email, password, birth]):
                    result = AccountsService.registry(DictHelper.parse_python_dict(AccountsMapping(data=request.data)))
                    if result:
                        return BaseResponse.success(data=AccountsMapping(result).data)
                    return BaseResponse.custom(status.HTTP_401_UNAUTHORIZED, "Đăng ký thất bại")
                return BaseResponse.error(message= "Thiếu thông tin đăng ký")
            
            if action and action == "restock-token":
                token = request.data.get("token")
                if token:
                    result = AccountsService.restock_token(token)
                    if result:
                        account = result.get("account")
                        if account:
                            if not account.is_active:
                                result["account"] = None
                                return BaseResponse.success(message="deactivated", data=result)
                            result["account"] = AccountsMapping(result.get("account")).data
                            return BaseResponse.success(data=result)
                    return BaseResponse.custom(status_code=status.HTTP_401_UNAUTHORIZED, message="Token không hợp lệ")
                return BaseResponse.error(message="Thiếu token")            
            return BaseResponse.internal(message=str(e))
        except Exception as e:
            return BaseResponse.internal(message=str(e))