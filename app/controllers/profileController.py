from rest_framework.views import APIView
from app.services.accountService import AccountService
from app.services.profileService import ProfileService
from app.mapping.profileMapping import ProfileMapping
from app.utils.parseBool import ParseBool
from app.utils.baseResponse import BaseResponse


class ProfileController(APIView):

    async def post(self, request, action=None):
        try:           
            if action and action == "all-users":
                page = request.data.get("page", "1")
                page_size = request.data.get("page_size", "20")
                is_active = ParseBool(request.data.get("is_active", "True"))

                result = await ProfileService.get_all(page=int(page), page_size=int(page_size), is_active=is_active)
                if result:
                    result["content"] = ProfileMapping(result.get("content", []), many=True).data
                    return BaseResponse.success(data=result)
                return BaseResponse.not_found()
            
            if action and action == "find-by-id":
                profile_id = request.data.get("profile_id", None)
                is_active = ParseBool(request.data.get("is_active", "True"))
                if profile_id:
                    result = await ProfileService.get_by_id(profile_id=profile_id, is_active=is_active)
                    if result:
                        return BaseResponse.success(data=ProfileMapping(result).data)
                    return BaseResponse.not_found()
                return BaseResponse.error(message="invalid_data")

            if action and action == "search":
                data = request.data.get("search_data")
                page = int(request.data.get("page", "1"))
                page_size = int(request.data.get("page_size", "20"))
                is_active = ParseBool(request.data.get("is_active", "True"))

                if data:
                    result = None
                    if AccountService.is_valid_email(str(data)):
                        account = await AccountService.get_by_email(email=str(data), is_active=is_active)
                        if account:
                            result = account.profile
                    if not result:
                        result = await ProfileService.get_by_nickname(nickname=str(data), page=page, page_size=page_size, is_active=is_active)

                    if result:
                        if isinstance(result, dict):
                            result["content"] = ProfileMapping(result.get("content", []), many=True).data
                            return BaseResponse.success(data=result)
                        return BaseResponse.success(data=ProfileMapping(result).data)
                    return BaseResponse.not_found()
                return BaseResponse.error(message="invalid_data")

            return BaseResponse.error(message="invalid_endpoint")
        except Exception as e:
            return BaseResponse.internal(data=str(e))
