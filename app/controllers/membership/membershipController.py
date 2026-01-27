from django.views import View

from app.dtos.membershipDTO import GetMembershipByIdDTO, SearchMembershipDTO
from app.enums.responseCodes import ResponseCodes
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.mapping.profileConversationMapping import ProfileConversationMapping
from app.services.profileConversationService import ProfileConversationService
from app.utils.requestData import RequestData


class MembershipController(View):
    async def get(self, request, membership_id=None):
        try:
            if membership_id:
                membership_dto = GetMembershipByIdDTO(membership_id=membership_id)

                result = await ProfileConversationService.get_by_id(membership_id=membership_dto.membership_id, is_active=True)
                return BaseResponse.success(
                    data=ProfileConversationMapping(result).data,
                    code=ResponseCodes.GET_MEMBERSHIP_BY_ID_SUCCESS,
                    message="Get membership by id successfully",
                )
            
            raw_data = RequestData(request=request)
            search_memberships_dto = SearchMembershipDTO(**raw_data)

            result = await ProfileConversationService.search_memberships(search_data=search_memberships_dto.model_dump())

            return BaseResponse.success(
                data=ProfileConversationMapping(result).data,
                code=ResponseCodes.SEARCH_MEMBERSHIP_SUCCESS,
                message="Search memberships successfully",
                page=result.get("page"),
                page_size=result.get("page_size"),
                total=result.get("total"),
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)