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
    async def get(self, request, relation_id=None):
        try:
            data = RequestData(request=request)

            if relation_id:
                dto = GetRelationByIdDTO(relation_id=relation_id)

                result = await RelationService.get_by_id(relation_id=dto.relation_id, is_active=True)
                return BaseResponse.success(
                    data=RelationMapping(result).data,
                    code=ResponseCodes.GET_RELATION_BY_ID_SUCCESS,
                    message="Get relation by id successfully",
                )
            
# viết hàm search

            # get_by_both_users_dto = GetRelationByProfilesDTO(**data)
            # result = await RelationService.get_by_both_users(get_by_both_users_dto)
            # return BaseResponse.success(
            #     data=RelationMapping(result).data,
            #     code=ResponseCodes.GET_RELATION_BY_BOTH_USERS_SUCCESS,
            #     message="Get relation by both users successfully",
            # )

                
            # user_id = data.get("user_id")
            # page = int(data.get("page", "1"))
            # page_size = int(data.get("page_size", "20"))
            # is_active = ParseBool(data.get("is_active", "True"))

            # if user_id:
            #     result = await RelationService.get_by_one_user(
            #         user_id, page=page, page_size=page_size, is_active=is_active
            #     )
            #     result["content"] = RelationMapping(
            #         result.get("content", []), many=True
            #     ).data
            #     return BaseResponse.send(data=result)
            # ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
