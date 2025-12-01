from django.views import View

from app.enums.responseMessages import ResponseMessages
from app.mapping.messageMapping import MessageMapping
from app.services.messageService import MessageService
from app.utils.baseResponse import BaseResponse
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.logHelper import LogHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData


class MessageController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)

            if action == "get-by-id":
                message_id = data.get("message_id")
                is_active = ParseBool(data.get("is_active", "true"))
                if message_id:
                    result = MessageService.get_by_id(
                        message_id=message_id, is_active=is_active
                    )
                    return BaseResponse.send(data=MessageMapping(result).data)
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            if action == "load-conversation-messages":
                conversation_id = data.get("conversation_id")
                page = int(data.get("page"))
                page_size = int(data.get("page_size"))
                is_active = ParseBool(data.get("is_active", "true"))

                if conversation_id:
                    result = MessageService.get_by_conversation(
                        conversation_id=conversation_id,
                        page=page,
                        page_size=page_size,
                        is_active=is_active,
                    )
                    result["content"] = MessageMapping(
                        result.get("content", []), many=True
                    ).data
                    return BaseResponse.send(data=result)
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            if action == "get-last-message":
                conversation_id = data.get("conversation_id")
                if conversation_id:
                    result = MessageService.get_last_conversation_message(
                        conversation_id=conversation_id
                    )
                    return BaseResponse.send(data=MessageMapping(result).data)
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_ENDPOINT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
