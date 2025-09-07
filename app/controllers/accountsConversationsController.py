# from rest_framework.views import APIView
# from app.mapping.accountsConversationsMapping import AccountsConversationsMapping
# from app.utils.baseResponse import BaseResponse
# from app.services.accountsConversationsService import AccountsConversationsService
# from app.mapping.conversationsMapping import ConversationsMapping


# class AccountsConversationsController(APIView):
#     def post(self, request, action):
#         try:
#             if action and action == "load-account-conversations":
#                 data = request.data
#                 data["account_id"] = str(request.user_id)
#                 response = AccountsConversationsService.find_by_account_paginated(data=data)
#                 list_ac = response["page_content"]
#                 result = [ac.get_conversation for ac in list_ac]
#                 response["page_content"] = ConversationsMapping(result, many=True).data
#                 return BaseResponse.success(data=response)
            
#             if action and action == "get-by-id":
#                 id = request.data.get("account_conversation_id")
#                 result = AccountsConversationsService.find_by_id(ac_id=id)
#                 if result:
#                     return BaseResponse.success(data=AccountsConversationsMapping(result).data)
                
#             if action and action == "get-by-conversation-id":
#                 id = request.data.get("conversation_id")
#                 result = AccountsConversationsService.find_by_conversation(conversation_id=id)
#                 if result:
#                     return BaseResponse.success(data=AccountsConversationsMapping(result).data)
#             return BaseResponse.error()
#         except Exception as e:
#             return BaseResponse.internal(message=f"lỗi ở đây {str(e)}")