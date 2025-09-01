from rest_framework.views import APIView
from app.services.relationService import RelationService
from app.mapping.relationMapping import RelationMapping
from app.utils.parseBool import ParseBool
from app.utils.baseResponse import BaseResponse

class RelationController(APIView):
    async def post(self, request, action=None):
        try:
            if action and action == "find-by-id":
                relation_id = request.data.get("relation_id")
                is_active = ParseBool(request.data.get("is_active", "True"))

                if relation_id:
                    result = await RelationService.get_by_id(relation_id, is_active=is_active)
                    if result:
                        return BaseResponse.success(data=RelationMapping(result).data)
                    return BaseResponse.not_found()
                return BaseResponse.error(message="invalid_data")

            if action and action == "find-by-both-users":
                user1_id = request.data.get("first_user_id")
                user2_id = request.data.get("second_user_id")
                is_active = ParseBool(request.data.get("is_active", "True"))

                if user1_id and user2_id:
                    result = await RelationService.get_by_both_users(user1_id, user2_id, is_active=is_active)
                    if result:
                        return BaseResponse.success(data=RelationMapping(result).data)
                    return BaseResponse.not_found()
                return BaseResponse.error(message="invalid_data")

            if action and action == "find-by-user":
                user_id = request.data.get("user_id")
                page = int(request.data.get("page", "1"))
                page_size = int(request.data.get("page_size", "20"))
                is_active = ParseBool(request.data.get("is_active", "True"))

                if user_id:
                    result = await RelationService.get_by_one_user(user_id, page=page, page_size=page_size, is_active=is_active)
                    if result:
                        result["content"] = RelationMapping(result.get("content", []), many=True).data
                        return BaseResponse.success(data=result)
                    return BaseResponse.not_found()
                return BaseResponse.error(message="invalid_data")

            if action and action == "create":
                first_user_id = request.data.get("first_user_id")
                second_user_id = request.data.get("second_user_id")

                if first_user_id and second_user_id:
                    result = await RelationService.create(request.data)
                    if result:
                        return BaseResponse.success(data=RelationMapping(result).data)
                    return BaseResponse.error(message="create_failed")
                return BaseResponse.error(message="invalid_data")

            if action and action == "update":
                relation_id = request.data.get("relation_id")
                if relation_id:
                    result = await RelationService.update(request.data)
                    if result:
                        return BaseResponse.success(data=RelationMapping(result).data)
                    return BaseResponse.error(message="update_failed")
                return BaseResponse.error(message="invalid_data")

            if action and action == "delete":
                relation_id = request.data.get("relation_id")
                if relation_id:
                    result = await RelationService.delete(relation_id)
                    if result:
                        return BaseResponse.success(data=RelationMapping(result).data)
                    return BaseResponse.error(message="delete_failed")
                return BaseResponse.error(message="invalid_data")

            return BaseResponse.error(message="invalid_endpoint")
        except Exception as e:
            return BaseResponse.internal(data=str(e))
