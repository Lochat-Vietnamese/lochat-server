from django.views import View

from app.dtos.messageDTOs import GetLastMessageDTO, GetMessageByConversationDTO, GetMessageByIdDTO
from app.enums.responseMessages import ResponseMessages
from app.mapping.messageMapping import MessageMapping
from app.services.messageService import MessageService
from app.utils.baseResponse import BaseResponse
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData


class MessageController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)

            if action == "get-by-id":
                dto = GetMessageByIdDTO(**data)
                
                result = MessageService.get_by_id(dto)
                return BaseResponse.send(data=MessageMapping(result).data)

            if action == "load-conversation-messages":
                dto = GetMessageByConversationDTO(**data)

                result = MessageService.get_by_conversation(dto)
                result["content"] = MessageMapping(
                    result.get("content", []), many=True
                ).data
                return BaseResponse.send(data=result)

            if action == "get-last-message":
                dto = GetLastMessageDTO(**data)
                result = MessageService.get_last_conversation_message(dto)
                return BaseResponse.send(data=MessageMapping(result).data)

            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_ENDPOINT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
