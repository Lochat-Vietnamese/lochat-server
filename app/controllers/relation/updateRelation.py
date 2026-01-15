from django.views import View

from app.dtos.relationDTOs import GetRelationByIdDTO, GetRelationByProfilesDTO
from app.enums.httpStatus import HttpStatus
from app.enums.responseCodes import ResponseCodes
from app.mapping.relationMapping import RelationMapping
from app.services.relationService import RelationService
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData


class RelationController(View):
    async def patch(self, request):
        try:
            # apply validator
            data = RequestData(request=request)

            relation_id = data.get("id")
            if relation_id:
                result = await RelationService.update(data)
                return BaseResponse.success(
                    data=RelationMapping(result).data,
                    code=ResponseCodes.UPDATE_RELATION_SUCCESS,
                    message="Update relation successfully",
                )
            ExceptionHelper.throw_bad_request("Missing relation id")

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
