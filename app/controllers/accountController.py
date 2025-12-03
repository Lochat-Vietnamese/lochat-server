from django.views import View

from app.enums.responseMessages import ResponseMessages
from app.services.accountService import AccountService
from app.mapping.accountMapping import AccountMapping
from app.utils.baseResponse import BaseResponse
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData


class AccountController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)

            if action == "get-by-id":
                account_id = data.get("account_id")
                is_active = ParseBool(data.get("is_active", "true"))

                if not account_id:
                    ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

                result = await AccountService.get_by_id( str(account_id), is_active=is_active)
                return BaseResponse.send(data=AccountMapping(result).data)

            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_ENDPOINT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)