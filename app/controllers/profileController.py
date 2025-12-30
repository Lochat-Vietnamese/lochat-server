from django.views import View

from app.dtos.profileDTOs import GetAllProfileDTO, GetProfileByIdDTO
from app.enums.responseMessages import ResponseMessages
from app.mapping.profileMapping import ProfileMapping
from app.services.accountService import AccountService
from app.services.profileService import ProfileService
from app.utils.baseResponse import BaseResponse
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData

class ProfileController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)
                
            if action == "all-users":
                dto = GetAllProfileDTO(**data)

                result = await ProfileService.get_all(dto)
                result["content"] = ProfileMapping(result.get("content", []), many=True).data
                return BaseResponse.send(data=result)
            
            if action == "get-by-id":
                dto = GetProfileByIdDTO(**data)
                result = await ProfileService.get_by_id(dto)
                return BaseResponse.send(data=ProfileMapping(result).data)

# làm lại sau khi tổ chức restful api
            # if action == "search":
            #     search_data = data.get("search_data")
            #     page = int(data.get("page", "1"))
            #     page_size = int(data.get("page_size", "20"))
            #     is_active = ParseBool(data.get("is_active", "True"))

            #     if search_data:
            #         result = None
            #         if AccountService.is_valid_email(str(search_data)):
            #             account = await AccountService.get_by_email(email=search_data, is_active=is_active)
            #             result = account.profile
            #         if not result:
            #             result = await ProfileService.get_by_nickname(nickname=search_data, page=page, page_size=page_size, is_active=is_active)

            #         if result:
            #             if isinstance(result, dict):
            #                 result["content"] = ProfileMapping(result.get("content", []), many=True).data
            #                 return BaseResponse.send(data=result)
            #             return BaseResponse.send(data=ProfileMapping(result).data)
            #     ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)
                

            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_ENDPOINT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)