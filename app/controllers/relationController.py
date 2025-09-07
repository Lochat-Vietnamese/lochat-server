from django.views import View

from app.mapping.relationMapping import RelationMapping
from app.services.relationService import RelationService
from app.utils.baseResponse import BaseResponse
from app.utils.logHelper import LogHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData

class RelationController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)
                

            if action == "find-by-id":
                relation_id = data.get("relation_id")
                is_active = ParseBool(data.get("is_active", "True"))

                if relation_id:
                    result = await RelationService.get_by_id(relation_id, is_active=is_active)
                    if result:
                        return BaseResponse.success(data=RelationMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()

            if action == "find-by-both-users":
                user1_id = data.get("first_user_id")
                user2_id = data.get("second_user_id")
                is_active = ParseBool(data.get("is_active", "True"))

                if user1_id and user2_id:
                    result = await RelationService.get_by_both_users(user1_id, user2_id, is_active=is_active)
                    if result:
                        return BaseResponse.success(data=RelationMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()

            if action == "find-by-user":
                user_id = data.get("user_id")
                page = int(data.get("page", "1"))
                page_size = int(data.get("page_size", "20"))
                is_active = ParseBool(data.get("is_active", "True"))

                if user_id:
                    result = await RelationService.get_by_one_user(user_id, page=page, page_size=page_size, is_active=is_active)
                    if result:
                        result["content"] = RelationMapping(result.get("content", []), many=True).data
                        return BaseResponse.success(data=result)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()

            if action == "create":
                first_user_id = data.get("first_user_id")
                second_user_id = data.get("second_user_id")

                if first_user_id and second_user_id:
                    result = await RelationService.create(data)
                    if result:
                        return BaseResponse.success(data=RelationMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()

            if action == "update":
                relation_id = data.get("relation_id")
                if relation_id:
                    result = await RelationService.update(data)
                    if result:
                        return BaseResponse.success(data=RelationMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()

            if action == "delete":
                relation_id = data.get("relation_id")
                if relation_id:
                    result = await RelationService.delete(relation_id)
                    if result:
                        return BaseResponse.success(data=RelationMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()
            

            return BaseResponse.error(message="invalid_endpoint")
        except Exception as e:
            LogHelper.error(message=str(e))
            return BaseResponse.internal(data=str(e))