from django.views import View

from app.dtos.authDTOs import SignUpDTO
from app.enums.httpStatus import HttpStatus
from app.enums.responseCodes import ResponseCodes
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.mapping.accountMapping import AccountMapping
from app.services.accountService import AccountService
from app.utils.requestData import RequestData


class SignUp(View):
    async def post(self, request):
        try:
            raw_data = RequestData(request=request)
            sign_up_dto = SignUpDTO(**raw_data)

            result = await AccountService.sign_up(sign_up_dto.model_dump())
            return BaseResponse.success(data=AccountMapping(result).data, code=ResponseCodes.SIGN_UP_SUCCESS, message="Sign up successfully", status_code=HttpStatus.CREATED)

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)