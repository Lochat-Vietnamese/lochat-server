from django.views import View

from app.mapping.profileMapping import ProfileMapping
from app.services.accountService import AccountService
from app.services.profileService import ProfileService
from app.utils.baseResponse import BaseResponse
from app.utils.logHelper import LogHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData

class ProfileController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)
                
            if action == "all-users":
                page = data.get("page", "1")
                page_size = data.get("page_size", "20")
                is_active = ParseBool(data.get("is_active", "True"))

                result = await ProfileService.get_all(page=int(page), page_size=int(page_size), is_active=is_active)
                if result:
                    result["content"] = ProfileMapping(result.get("content", []), many=True).data
                    return BaseResponse.success(data=result)
                return BaseResponse.error(message="process_failed")
            
            if action == "find-by-id":
                profile_id = data.get("profile_id", None)
                is_active = ParseBool(data.get("is_active", "True"))
                if profile_id:
                    result = await ProfileService.get_by_id(profile_id=profile_id, is_active=is_active)
                    if result:
                        return BaseResponse.success(data=ProfileMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()

            if action == "search":
                search_data = data.get("search_data")
                page = int(data.get("page", "1"))
                page_size = int(data.get("page_size", "20"))
                is_active = ParseBool(data.get("is_active", "True"))

                if search_data:
                    result = None
                    if AccountService.is_valid_email(str(search_data)):
                        account = await AccountService.get_by_email(email=search_data, is_active=is_active)
                        if account:
                            result = account.profile
                    if not result:
                        result = await ProfileService.get_by_nickname(nickname=search_data, page=page, page_size=page_size, is_active=is_active)

                    if result:
                        if isinstance(result, dict):
                            result["content"] = ProfileMapping(result.get("content", []), many=True).data
                            return BaseResponse.success(data=result)
                        return BaseResponse.success(data=ProfileMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()
                

            return BaseResponse.error(message="invalid_endpoint")
        except Exception as e:
            LogHelper.error(message=str(e))
            return BaseResponse.internal(data=str(e))