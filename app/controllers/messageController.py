from django.views import View

from app.mapping.messageMapping import MessageMapping
from app.services.messageService import MessageService
from app.utils.baseResponse import BaseResponse
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
                    result = MessageService.get_by_id(message_id=message_id, is_active=is_active)
                    if result:
                        return BaseResponse.success(data=MessageMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()            

            if action == "load-conversation-messages":
                conversation_id = data.get("conversation_id")
                page=int(data.get("page"))
                page_size=int(data.get("page_size"))
                is_active = ParseBool(data.get("is_active", "true"))

                if conversation_id:
                    result = MessageService.get_by_conversation(conversation_id=conversation_id, page=page, page_size=page_size, is_active=is_active)
                    if result:
                        result["content"] = MessageMapping(
                            result.get("content", []), many=True
                        ).data
                        return BaseResponse.success(data=result)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error() 
            
            if action == "get-last-message":
                conversation_id = data.get("conversation_id")
                if conversation_id:
                    result = MessageService.get_last_conversation_message(conversation_id=conversation_id)
                    if result:
                        return BaseResponse.success(data=MessageMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error() 

            

            return BaseResponse.error(message="invalid_endpoint")
        except Exception as e:
            LogHelper.error(message=str(e))
            return BaseResponse.internal(data=str(e))