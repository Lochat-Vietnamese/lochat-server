from django.views import View

from app.dtos.relationDTOs import GetRelationByIdDTO, GetRelationByProfilesDTO
from app.enums.responseMessages import ResponseMessages
from app.mapping.relationMapping import RelationMapping
from app.services.relationService import RelationService
from app.utils.baseResponse import BaseResponse
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData


class RelationController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)

            if action == "get-by-id":
                dto = GetRelationByIdDTO(**data)

                result = await RelationService.get_by_id(dto)
                return BaseResponse.send(data=RelationMapping(result).data)

            if action == "get-by-both-users":
                dto = GetRelationByProfilesDTO(**data)
                result = await RelationService.get_by_both_users(dto)
                return BaseResponse.send(data=RelationMapping(result).data)

            if action == "get-by-user":
                
                user_id = data.get("user_id")
                page = int(data.get("page", "1"))
                page_size = int(data.get("page_size", "20"))
                is_active = ParseBool(data.get("is_active", "True"))

                if user_id:
                    result = await RelationService.get_by_one_user(
                        user_id, page=page, page_size=page_size, is_active=is_active
                    )
                    result["content"] = RelationMapping(
                        result.get("content", []), many=True
                    ).data
                    return BaseResponse.send(data=result)
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            if action == "create":
                first_user_id = data.get("first_user_id")
                second_user_id = data.get("second_user_id")

                if first_user_id and second_user_id:
                    result = await RelationService.create(data)
                    return BaseResponse.send(data=RelationMapping(result).data)
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            if action == "update":
                relation_id = data.get("id")
                if relation_id:
                    result = await RelationService.update(data)
                    return BaseResponse.send(data=RelationMapping(result).data)
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            if action == "block":
                relation_id = data.get("relation_id")
                if relation_id:
                    result = await RelationService.delete(relation_id)
                    return BaseResponse.send(data=RelationMapping(result).data)
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_ENDPOINT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
