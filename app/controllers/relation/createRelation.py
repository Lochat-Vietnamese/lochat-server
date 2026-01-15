from django.views import View

from app.enums.httpStatus import HttpStatus
from app.enums.responseCodes import ResponseCodes
from app.mapping.relationMapping import RelationMapping
from app.services.relationService import RelationService
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData


class RelationController(View):
    async def post(self, request):
        try:
            # apply validator
            data = RequestData(request=request)

            first_user_id = data.get("first_user_id")
            second_user_id = data.get("second_user_id")

            if first_user_id and second_user_id:
                result = await RelationService.create(data)
                return BaseResponse.success(
                    data=RelationMapping(result).data,
                    code=ResponseCodes.CREATE_RELATION_SUCCESS,
                    message="Create relation successfully",
                )
            ExceptionHelper.throw_bad_request("Missing data")

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
