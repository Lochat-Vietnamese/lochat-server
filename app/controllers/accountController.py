from django.views import View

from app.dtos.accountDTOs import GetByIdDTO
from app.enums.responseMessages import ResponseMessages
from app.services.accountService import AccountService
from app.mapping.accountMapping import AccountMapping
from app.utils.baseResponse import BaseResponse
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData


class AccountController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)

            if action == "get-by-id":
                dto = GetByIdDTO(**data)

                result = await AccountService.get_by_id(dto)
                return BaseResponse.send(data=AccountMapping(result).data)

            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_ENDPOINT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)