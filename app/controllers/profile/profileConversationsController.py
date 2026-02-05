from django.views import View
from app.dtos.profileDTOs import GetProfileConversationsDTO
from app.enums.httpStatus import HttpStatus
from app.enums.responseCodes import ResponseCodes
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.mapping.conversationMapping import ConversationMapping
from app.services.profileConversationService import ProfileConversationService
from app.utils.requestData import RequestData
from asgiref.sync import sync_to_async


class ProfileConversationsController(View):
    async def get(self, request, profile_id):
        try:
            if not profile_id:
                ExceptionHelper.throw_bad_request("Missing profile id")
                
            logging_in_profile_id = str(request.logging_in_profile)

            raw_data = RequestData(request=request)
            raw_data["profile_id"] = profile_id
            get_conversations_dto = GetProfileConversationsDTO(**raw_data)

            if get_conversations_dto.profile_id != logging_in_profile_id:
                return BaseResponse.error(
                    code=ResponseCodes.PERMISSION_DENIED,
                    message="permission denied",
                    status_code=HttpStatus.FORBIDDEN,
                    details="You don't have permission to get this profile's conversations"
                )
            result = await sync_to_async(ProfileConversationService.get_by_profile)(
                profile_id=get_conversations_dto.profile_id,
                page=get_conversations_dto.page,
                page_size=get_conversations_dto.page_size,
                is_active=get_conversations_dto.is_active,
            )
            profile_conversations = result["data"]
            conversations = [pc.conversation for pc in profile_conversations]

            list_conversations = ConversationMapping(conversations, many=True).data

            return BaseResponse.success(
                code=ResponseCodes.GET_PROFILE_CONVERSATION_SUCCESS,
                message="Load profile conversations successfully",
                page=result.get("page"),
                page_size=result.get("page_size"),
                total_items=result.get("total_items"),
                data=list_conversations
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)