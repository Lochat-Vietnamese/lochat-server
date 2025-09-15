from django.views import View

from app.mapping.conversationMapping import ConversationMapping
from app.services.conversationService import ConversationService
from app.utils.baseResponse import BaseResponse
from app.utils.logHelper import LogHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData

class ConversationController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)


            if action == "get-by-id":
                id = data.get("conversation_id")
                is_active = ParseBool(data.get("is_active", "true"))
                if id:
                    result = await ConversationService.get_by_id(conversation_id=id, is_active=is_active)
                    if result:
                        return BaseResponse.success(data=ConversationMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()
  

            return BaseResponse.error(message="invalid_endpoint")
        except Exception as e:
            LogHelper.error(message=str(e))
            return BaseResponse.internal(data=str(e))
