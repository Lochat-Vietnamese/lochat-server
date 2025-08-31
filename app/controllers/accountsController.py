from rest_framework.views import APIView
from rest_framework import status
from app.services.accountsService import AccountsService
from app.mapping.accountMapping import AccountsMapping
from app.utils.baseResponse import BaseResponse
from app.utils.dictHelper import DictHelper

class AccountsController(APIView):

    def post(self, request, action = None):
        try:
            if action and action == "search":
                data = str(request.data.get("search_data"))
                if data:
                    result = None
                    if "@" in data and "." in data and data.count("@") == 1:
                        result = AccountsService.find_by_email(data)
                        if not result:
                            result = AccountsService.find_by_nickname(data)
                    else:
                        result = AccountsService.find_by_nickname(data)
                    if result:
                        if isinstance(result, list):
                            return BaseResponse.success(data=AccountsMapping(result, many=True).data)
                        return BaseResponse.success(data=AccountsMapping(result).data)
                    return BaseResponse.not_found(message="Không tìm thấy tài khoản")
                return BaseResponse.error(message="Thông tin tìm kiếm không hợp lệ")
            
            if action and action == "find-by-id":
                data = str(request.data.get("account_id"))
                if data:
                    result = AccountsService.find_by_id(data)
                    if result:
                        return BaseResponse.success(data=AccountsMapping(result).data)
                    return BaseResponse.not_found(message="Không tìm thấy tài khoản")
                return BaseResponse.error(message="Thông tin tìm kiếm không hợp lệ")
            
            if action and action == "all-users":
                data = request.data or {}
                result = AccountsService.find_all_paginated(data)
                if result:
                    result["page_content"] = AccountsMapping(result.get("page_content", []), many=True).data
                    return BaseResponse.success(data=result)
                return BaseResponse.error(message="Dữ liệu không hợp lệ")
            
            return BaseResponse.internal(message=str(e))
        except Exception as e:
            return BaseResponse.internal(message=str(e))