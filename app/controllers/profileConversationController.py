from django.views import View

from app.mapping.profileConversationMapping import ProfileConversationMapping
from app.services.conversationService import ConversationService
from app.services.profileConversationService import ProfileConversationService
from app.utils.baseResponse import BaseResponse
from app.utils.logHelper import LogHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData

class ProfileConversationController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)

            if action == "load-profile-conversations":
                account_id = str(request.user_id)
                page = int(data.get("page", "1"))
                page_size = int(data.get("page_size", "20"))
                is_active = ParseBool(data.get("is_active", "true"))
                if account_id:
                    result = await ProfileConversationService.get_by_account(account_id=account_id, page=page, page_size=page_size, is_active=is_active)
                    if result:
                        list_ac = result["content"]
                        result = [ac.conversation for ac in list_ac]
                        result["content"] = ProfileConversationMapping(result, many=True).data
                        return BaseResponse.success(data=ProfileConversationMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()
            
            if action == "get-by-id":
                id = data.get("profile_conversation_id")
                if id:
                    result = await ProfileConversationService.get_by_id(profileConversation_id=id)
                    if result:
                            return BaseResponse.success(data=ProfileConversationMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()
                
            if action == "get-by-conversation":
                id = data.get("conversation_id")
                page = int(data.get("page", "1"))
                page_size = int(data.get("page_size", "20"))
                is_active = ParseBool(data.get("is_active", "true"))
                if id:
                    result = await ProfileConversationService.get_by_conversation(conversation_id=id, page=page, page_size=page_size, is_active=is_active)
                    if result:
                        return BaseResponse.success(data=ProfileConversationMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()


            return BaseResponse.error(message="invalid_endpoint")

        except Exception as e:
            LogHelper.error(message=str(e))
            return BaseResponse.internal(data=str(e))
