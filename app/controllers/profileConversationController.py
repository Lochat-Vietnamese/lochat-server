from django.views import View

from app.enums.responseMessages import ResponseMessages
from app.mapping.profileConversationMapping import ProfileConversationMapping
from app.services.profileConversationService import ProfileConversationService
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData

# tách ra đem qua profile và conversation
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
                    result = await ProfileConversationService.get_by_account(
                        account_id=account_id,
                        page=page,
                        page_size=page_size,
                        is_active=is_active,
                    )
                    list_ac = result["content"]
                    result = [ac.conversation for ac in list_ac]
                    result["content"] = ProfileConversationMapping(
                        result, many=True
                    ).data
                    return BaseResponse.send(
                        data=ProfileConversationMapping(result).data
                    )
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            if action == "get-by-id":
                id = data.get("profile_conversation_id")
                if id:
                    result = await ProfileConversationService.get_by_id(
                        profileConversation_id=id
                    )
                    return BaseResponse.send(
                        data=ProfileConversationMapping(result).data
                    )
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            if action == "get-by-conversation":
                id = data.get("conversation_id")
                page = int(data.get("page", "1"))
                page_size = int(data.get("page_size", "20"))
                is_active = ParseBool(data.get("is_active", "true"))
                if id:
                    result = await ProfileConversationService.get_by_conversation(
                        conversation_id=id,
                        page=page,
                        page_size=page_size,
                        is_active=is_active,
                    )
                    return BaseResponse.send(
                        data=ProfileConversationMapping(result).data
                    )
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_ENDPOINT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
