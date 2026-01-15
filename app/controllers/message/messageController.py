from django.views import View

from app.dtos.messageDTOs import SearchMessagesDTO, GetMessageByIdDTO
from app.enums.httpStatus import HttpStatus
from app.enums.responseCodes import ResponseCodes
from app.mapping.messageMapping import MessageMapping
from app.services.messageService import MessageService
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData


class MessageController(View):
    async def get(self, request, message_id=None):
        try:
            if message_id:
                message_dto = GetMessageByIdDTO(message_id=message_id)
                result = MessageService.get_by_id(message_id=message_dto.message_id)
                return BaseResponse.success(
                    data=MessageMapping(result).data,
                    code=ResponseCodes.GET_MESSAGE_BY_ID_SUCCESS,
                    message="Get message by id successfully",
                )
            
            data = RequestData(request=request)
            search_data = SearchMessagesDTO(**data)

            if search_data.get_last == True:
                result = MessageService.get_last_conversation_message(conversation_id=search_data.conversation_id)
                return BaseResponse.success(
                    data=MessageMapping(result).data,
                    code=ResponseCodes.GET_LAST_CONVERSATION_MESSAGE_SUCCESS,
                    message="Get last conversation message successfully",
                )
            
            # lam cai ham search tong de thay the (vua xu ly search vua get all)
            result = MessageService.get_by_conversation(
                conversation_id=search_data.conversation_id,
                page=search_data.page,
                page_size=search_data.page_size,
                is_active=search_data.is_active
            )
            
            result["content"] = MessageMapping(
                result.get("content", []), many=True
            ).data
            return BaseResponse.success(data=result)            
        
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
