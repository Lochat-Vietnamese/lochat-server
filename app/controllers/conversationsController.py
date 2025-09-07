# from rest_framework.views import APIView
# from app.mapping.conversationsMapping import ConversationsMapping
# from app.services.conversationsService import ConversationsService
# from app.utils.baseResponse import BaseResponse

# class ConversationsController(APIView):
#     def post(self, request, action):
#         try:
#             if action and action == "get-by-id":
#                 id = request.data.get("conversation_id")
#                 result = ConversationsService.find_by_id(conversation_id=id)
#                 if result:
#                     return BaseResponse.success(data=ConversationsMapping(result).data)
#                 return BaseResponse.error(message="Dữ liệu không hợp lệ")
           
#             return BaseResponse.internal()
#         except Exception as e:
#             return BaseResponse.internal(message=str(e))
