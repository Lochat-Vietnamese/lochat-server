from django.views import View

from app.dtos.relationDTOs import CreateRelationDTO, GetRelationByIdDTO, SearchRelationsDTO, UpdateRelationDTO
from app.enums.httpStatus import HttpStatus
from app.enums.responseCodes import ResponseCodes
from app.mapping.relationMapping import RelationMapping
from app.services.relationService import RelationService
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData


class RelationController(View):
    async def get(self, request, relation_id=None):
        try:
            if relation_id:
                dto = GetRelationByIdDTO(relation_id=relation_id)

                result = await RelationService.get_by_id(relation_id=dto.relation_id, is_active=True)
                return BaseResponse.success(
                    data=RelationMapping(result).data,
                    code=ResponseCodes.GET_RELATION_BY_ID_SUCCESS,
                    message="Get relation by id successfully",
                )
            
            raw_data = RequestData(request=request)
            search_relations_dto = SearchRelationsDTO(**raw_data)

            if search_relations_dto.is_only_pagination():
                result = await RelationService.get_all(page=search_relations_dto.page, page_size=search_relations_dto.page_size, is_active=search_relations_dto.is_active)
                return BaseResponse.success(
                    data=RelationMapping(result.get("data", []), many=True).data,
                    code=ResponseCodes.GET_ALL_RELATIONS_SUCCESS,
                    message="Get all relation successfully",
                    page=result.get("page"),
                    page_size=result.get("page_size"),
                    total_items=result.get("total_items"),
                )


            result = await RelationService.search_relations(search_relations_dto.model_dump())
            return BaseResponse.success(
                data=RelationMapping(result.get("data", []), many=True).data,
                code=ResponseCodes.SEARCH_RELATION_SUCCESS,
                message="Search relation successfully",
                page=result.get("page"),
                page_size=result.get("page_size"),
                total_items=result.get("total_items"),
            )

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    async def post(self, request):
        try:
            raw_data = RequestData(request=request)
            create_relation_dto = CreateRelationDTO(**raw_data)

            result = await RelationService.create(create_relation_dto.model_dump())
            return BaseResponse.success(
                status_code=HttpStatus.CREATED,
                data=RelationMapping(result).data,
                code=ResponseCodes.CREATE_RELATION_SUCCESS,
                message="Create relation successfully",
            )

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    async def patch(self, request):
        try:
            raw_data = RequestData(request=request)
            update_relation_dto = UpdateRelationDTO(**raw_data)

            result = await RelationService.update(update_relation_dto.model_dump())
            return BaseResponse.success(
                data=RelationMapping(result).data,
                code=ResponseCodes.UPDATE_RELATION_SUCCESS,
                message="Update relation successfully",
            )

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
