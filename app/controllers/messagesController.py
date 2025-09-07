# from rest_framework.views import APIView
# from app.utils.baseResponse import BaseResponse
# from app.services.messagesService import MessagesService
# from app.mapping.messagesMapping import MessagesMapping


# class MessagesController(APIView):
#     def post(self, request, action):
#         try:
#             if action and action == "load-conversation-messages":
#                 conversation_id = request.data.get("conversation_id")

#                 if conversation_id:
#                     result = MessagesService.find_by_conversation(request.data)
#                     if result:
#                         result["page_content"] = MessagesMapping(
#                             result.get("page_content", []), many=True
#                         ).data
#                         return BaseResponse.success(data=result)
#                 return BaseResponse.error(message="Dữ liệu không hợp lệ")
            
#             if action and action == "get-last-message":
#                 conversation_id = request.data.get("conversation_id")
#                 if conversation_id:
#                     result = MessagesService.find_last_conversation_message(conversation_id)
#                     if result:
#                         return BaseResponse.success(data=MessagesMapping(result).data)
#                     return BaseResponse.error(message=f"No message found in conversation {conversation_id}")
#                 return BaseResponse.error(message="Dữ liệu không hợp lệ")
#             return BaseResponse.internal()

#         except Exception as e:
#             return BaseResponse.internal(message=str(e))
