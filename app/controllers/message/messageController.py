from django.views import View

from app.dtos.messageDTOs import SearchMessagesDTO, GetMessageByIdDTO
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
                result = await MessageService.get_by_id(message_id=message_dto.message_id)
                return BaseResponse.success(
                    data=MessageMapping(result).data,
                    code=ResponseCodes.GET_MESSAGE_BY_ID_SUCCESS,
                    message="Get message by id successfully",
                )
            
            raw_data = RequestData(request=request)
            search_messages_dto = SearchMessagesDTO(**raw_data)

            if search_messages_dto.is_only_pagination():
                result = await MessageService.get_all(page=search_messages_dto.page, page_size=search_messages_dto.page_size, is_active=search_messages_dto.is_active)
                return BaseResponse.success(
                    data=MessageMapping(result.get("data", []), many=True).data,
                    code=ResponseCodes.SEARCH_PROFILE_SUCCESS,
                    message="Search profile successfully",
                    page=result.get("page"),
                    page_size=result.get("page_size"),
                    total_items=result.get("total_items"),
                )

            if search_messages_dto.get_last == True:
                result = await MessageService.get_last_conversation_message(conversation_id=search_messages_dto.conversation_id)
                return BaseResponse.success(
                    data=MessageMapping(result).data,
                    code=ResponseCodes.GET_LAST_CONVERSATION_MESSAGE_SUCCESS,
                    message="Get last conversation message successfully",
                )
            
            result = await MessageService.search_messages(search_messages_dto.model_dump())
            return BaseResponse.success(
                data=MessageMapping(result.get("data", []), many=True).data,
                code=ResponseCodes.SEARCH_PROFILE_SUCCESS,
                message="Search profile successfully",
                page=result.get("page"),
                page_size=result.get("page_size"),
                total_items=result.get("total_items"),
            )
           
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
