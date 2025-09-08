# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# from app.services.accountsConversationsService import AccountsConversationsService
# from app.services.conversationsService import ConversationsService
# from django.contrib.auth.models import AnonymousUser
# from app.services.accountsService import AccountsService
# from app.enums.messageTypes import MessageTypes
# from app.utils.redisClient import RedisClient
# from asgiref.sync import sync_to_async


# class ChatConsumer(AsyncWebsocketConsumer):
#     _room_id = None
#     _current_user = None
#     _current_sender_relation = None

#     async def exception_send(self, exception=""):
#         await self.send(
#             text_data=json.dumps(
#                 {"error": "Dữ liệu gửi lên không hợp lệ", "detail": str(exception)},
#                 ensure_ascii=False,
#             )
#         )

#     async def connect_room(self, conversation, *accounts):
#         self._room_id = str(conversation.id)
#         self._current_sender_relation = await sync_to_async(
#             AccountsConversationsService.find_by_account_and_conversation
#         )({"conversation_id": self._room_id, "account_id": self._current_user.id})
#         await self.channel_layer.group_add(self._room_id, self.channel_name)
#         await self.accept()
#         for acc in accounts:
#             await self.send(
#                 json.dumps(
#                     {
#                         "message": (
#                             f"room id: {self._room_id}"
#                             + f"Đã kết nối với {acc.nickname}"
#                             if acc != self.scope["user"]
#                             else "Đã kết nối"
#                         )
#                     },
#                     ensure_ascii=False,
#                 )
#             )

#     async def text(self, event):
#         await self.send(
#             text_data=json.dumps(
#                 {
#                     "content": event["content"],
#                     "sender": event["sender"],
#                 },
#                 ensure_ascii=False,
#             )
#         )

#     async def media(self, event):
#         await self.send(
#             text_data=json.dumps(
#                 {
#                     "content": event["content"],
#                     "sender": event["sender"],
#                     "media": event["media"],
#                 },
#                 ensure_ascii=False,
#             )
#         )

#     async def connect(self):
#         try:
#             router = self.scope["url_route"]["kwargs"]
#             id = str(router["id"])
#             self._current_user = self.scope["user"]
#             if isinstance(self._current_user, AnonymousUser):
#                 await self.accept()
#                 await self.send(
#                     json.dumps({"message": "Vui lòng đăng nhập"}, ensure_ascii=False)
#                 )
#                 await self.close()
#             else:
#                 represent_conversation = await sync_to_async(
#                     ConversationsService.find_by_id
#                 )(id)
#                 if not represent_conversation:
#                     friend = await sync_to_async(AccountsService.find_by_id)(id)
#                     if friend:
#                         common_conversation = await sync_to_async(
#                             AccountsConversationsService.find_common_conversation
#                         )(self._current_user.id, id)
#                         if not common_conversation:
#                             new_conversation = await sync_to_async(
#                                 ConversationsService.create
#                             )({})
#                             await sync_to_async(AccountsConversationsService.create)(
#                                 {
#                                     "account": str(self._current_user.id),
#                                     "conversation": str(new_conversation.id),
#                                 }
#                             )
#                             await sync_to_async(AccountsConversationsService.create)(
#                                 {
#                                     "account": str(friend.id),
#                                     "conversation": str(new_conversation.id),
#                                 }
#                             )
#                             await self.connect_room(
#                                 new_conversation, self._current_user, friend
#                             )
#                         else:
#                             await self.connect_room(
#                                 common_conversation, self._current_user, friend
#                             )
#                     else:
#                         await self.accept()
#                         await self.send(
#                             json.dumps(
#                                 {
#                                     "message": f"Không tìm thấy tài khoản hoặc đoạn chat {id}"
#                                 },
#                                 ensure_ascii=False,
#                             )
#                         )
#                 else:
#                     await self.connect_room(represent_conversation, self._current_user)
#         except Exception as e:
#             await self.accept()
#             await self.send(
#                 json.dumps(
#                     {"error": "Lỗi trong quá trình kết nối", "detail": str(e)},
#                     ensure_ascii=False,
#                 )
#             )

#     async def receive(self, text_data):
#         try:
#             received = json.loads(text_data)
#             type = received.get("type", "text")
#             data = received.get("content", "")
#             reply = received.get("reply_to", None)
#             if type in MessageTypes.values:
#                 if type == MessageTypes.MEDIA:
#                     name = received.get("name", None)
#                     media_type = received.get("media_type", None)
#                     size = received.get("size", None)
#                     url = received.get("url", None)
#                     message_data = {
#                         "sender_relation_id": str(self._current_sender_relation.id),
#                         "type": type,
#                         "content": str(data),
#                         "media_name": name,
#                         "media_type": media_type,
#                         "media_size": size,
#                         "media_url": url,
#                     }
#                 else:
#                     message_data = {
#                         "sender_relation_id": str(self._current_sender_relation.id),
#                         "type": type,
#                         "content": str(data),
#                     }
#                 if reply and str(reply).strip():
#                     message_data["reply_to"] = str(reply)
#                 await sync_to_async(RedisClient.instance().queue_add)(
#                     "message_queue", message_data
#                 )
#             else:
#                 await self.exception_send()
#         except Exception as e:
#             await self.exception_send(e)

#     async def disconnect(self, _=None):
#         try:
#             if self._room_id:
#                 await self.channel_layer.group_discard(self._room_id, self.channel_name)
#         except Exception as e:
#             try:
#                 await self.send(
#                     json.dumps(
#                         {"error": "Lỗi trong quá trình ngắt kết nối", "detail": str(e)},
#                         ensure_ascii=False,
#                     )
#                 )
#             except:
#                 pass
