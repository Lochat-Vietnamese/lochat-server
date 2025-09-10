from django.views import View

from app.services.accountService import AccountService
from app.mapping.accountMapping import AccountMapping
from app.utils.baseResponse import BaseResponse
from app.utils.logHelper import LogHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData

class AccountController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)


            if action == "find-by-id":
                account_id = data.get("account_id")
                is_active = ParseBool(data.get("is_active", "true"))

                if account_id:
                    result = await AccountService.get_by_id(
                        str(account_id), is_active=is_active
                    )
                    if result:
                        return BaseResponse.success(data=AccountMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()
            

            return BaseResponse.error(message="invalid_endpoint")
        except Exception as e:
            LogHelper.error(message=str(e))
            return BaseResponse.internal(data=str(e))