from django.views import View

from app.dtos.accountDTOs import GetAccountByIdDTO
from app.enums.responseCodes import ResponseCodes
from app.enums.responseMessages import ResponseMessages
from app.services.accountService import AccountService
from app.mapping.accountMapping import AccountMapping
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData


class AccountController(View):
    async def get(self, request, account_id=None):
        try:
            if account_id:
                dto = GetAccountByIdDTO(account_id=account_id)

                result = await AccountService.get_by_id(account_id=dto.account_id)
                return BaseResponse.success(
                    data=AccountMapping(result).data,
                    code=ResponseCodes.GET_ACCOUNT_BY_ID_SUCCESS,
                    message="Get account by id successfully",
                )

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)