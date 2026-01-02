from django.views import View

from app.dtos.conversationDTOs import GetConversationByIdDTO
from app.enums.responseMessages import ResponseMessages
from app.mapping.conversationMapping import ConversationMapping
from app.services.conversationService import ConversationService
from app.utils.baseResponse import BaseResponse
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData


class ConversationController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)

            if action == "get-by-id":
                dto = GetConversationByIdDTO(**data)
                
                result = await ConversationService.get_by_id(dto)
                return BaseResponse.send(data=ConversationMapping(result).data)

            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_ENDPOINT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
