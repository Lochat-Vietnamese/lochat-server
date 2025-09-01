from rest_framework.views import APIView
from app.services.accountService import AccountService
from app.mapping.accountMapping import AccountMapping
from app.utils.dictHelper import DictHelper
from app.utils.parseBool import ParseBool
from app.utils.baseResponse import BaseResponse


class AccountController(APIView):

    async def post(self, request, action=None):
        try:
            if action and action == "find-by-id":
                account_id = request.data.get("account_id")
                is_active = ParseBool(request.data.get("is_active", "true"))

                if account_id:
                    result = await AccountService.get_by_id(
                        str(account_id), is_active=is_active
                    )
                    if result:
                        return BaseResponse.success(data=AccountMapping(result).data)
                    return BaseResponse.not_found()
                return BaseResponse.error(message="invalid_data")

            return BaseResponse.error(message="invalid_endpoint")
        except Exception as e:
            return BaseResponse.internal(data=str(e))
