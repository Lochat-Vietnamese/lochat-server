from django.views import View

from app.dtos.conversationDTOs import GetConversationByIdDTO
from app.enums.responseCodes import ResponseCodes
from app.mapping.conversationMapping import ConversationMapping
from app.services.conversationService import ConversationService
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from asgiref.sync import sync_to_async


class ConversationController(View):
    async def get(self, request, conversation_id=None):
        try:
            if conversation_id:
                conversattion_dto = GetConversationByIdDTO(conversation_id=conversation_id)
                
                result = await sync_to_async(ConversationService.get_by_id)(conversattion_dto.conversation_id)
                return BaseResponse.success(
                    data=ConversationMapping(result).data,
                    code=ResponseCodes.GET_CONVERSATION_BY_ID_SUCCESS,
                    message="Get conversation by id successfully",
                )

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
