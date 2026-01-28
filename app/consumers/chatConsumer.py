from channels.generic.websocket import AsyncWebsocketConsumer
import json
from app.enums.conversationTypes import ConversationTypes
from app.services.profileConversationService import ProfileConversationService
from app.services.conversationService import ConversationService
from django.contrib.auth.models import AnonymousUser
from app.enums.messageTypes import MessageTypes
from app.services.profileService import ProfileService
from app.utils.logHelper import LogHelper
from app.infrastructures.redis.redisClient import RedisClient


class ChatConsumer(AsyncWebsocketConsumer):
    _room_id = None
    _current_user = None
    _current_sender_relation = None
    _redis_instance = None

    async def exception_send(self):
        await self.send(
            text_data=json.dumps(
                {"message": "invalid_data", "data": None},
                ensure_ascii=False,
            )
        )

    async def connect_room(self, conversation, *profiles):
        self._redis_instance = await RedisClient.instance()
        self._room_id = str(conversation.id)
        self._current_sender_relation = await ProfileConversationService.get_by_both(
            conversation_id=self._room_id,
            profile_id=self._current_user.id,
            is_active=True,
        )

        await self.channel_layer.group_add(self._room_id, self.channel_name)
        await self.accept()
        
        for _ in profiles:
            await self.send(
                json.dumps(
                    {
                        "message": "connected",
                        "data": self._room_id                        
                    },
                    ensure_ascii=False,
                )
            )

    async def connect(self):
        try:
            router = self.scope["url_route"]["kwargs"]
            path_id = str(router["id"])
            self._current_user = self.scope["user"]
            if isinstance(self._current_user, AnonymousUser):
                await self.accept()
                await self.send(
                    json.dumps({"message": "Vui lòng đăng nhập"}, ensure_ascii=False)
                )
                await self.close()
            else:
                represent_conversation = await ConversationService.get_by_id(
                    conversation_id=path_id
                )
                if not represent_conversation:
                    friend = await ProfileService.get_by_id(profile_id=path_id, is_active=True)
                    if friend:
                        common_conversation = (
                            await ProfileConversationService.get_common_conversations(
                                profile1_id=self._current_user.id,
                                profile2_id=path_id,
                                is_active=True,
                                type=ConversationTypes.PRIVATE,
                            )
                        )
                        if not common_conversation:
                            new_conversation = await ConversationService.create(
                                {"creator_id": str(self._current_user.id)}
                            )
                            await ProfileConversationService.create(
                                {
                                    "profile_id": str(self._current_user.id),
                                    "conversation_id": str(new_conversation.id),
                                    "conversation_name": friend.nickname,
                                }
                            )
                            await ProfileConversationService.create(
                                {
                                    "profile_id": str(friend.id),
                                    "conversation_id": str(new_conversation.id),
                                    "conversation_name": self._current_user.nickname,
                                }
                            )
                            await self.connect_room(
                                new_conversation, self._current_user, friend
                            )
                        else:
                            await self.connect_room(
                                common_conversation, self._current_user, friend
                            )
                    else:
                        await self.accept()
                        await self.send(
                            json.dumps(
                                {"message": "not_found", "data": "friend not found"},
                                ensure_ascii=False,
                            )
                        )
                else:
                    await self.connect_room(represent_conversation, self._current_user)
        except Exception as e:
            await self.accept()
            await self.send(
                json.dumps(
                    {"message": "connection_error", "data": str(e)},
                    ensure_ascii=False,
                )
            )
            LogHelper.error(message=str(e))

    async def text(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": "success",
                    "data": {
                        "content": event["content"],
                        "sender": event["sender"],
                        "reply": event["reply"]
                    },
                },
                ensure_ascii=False
            )
        )

    async def media(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": "success",
                    "data": {
                        "content": event["content"],
                        "sender": event["sender"],
                        "media": event["media"],
                        "reply": event["reply"]
                    },
                },
                ensure_ascii=False,
            )
        )

    async def receive(self, text_data):
        try:
            received = json.loads(text_data)
            type = received.get("type", "text")
            data = received.get("content", "")
            reply = received.get("reply", None)

            if type in MessageTypes.values:
                if type == MessageTypes.MEDIA:
                    name = received.get("name", None)
                    media_type = received.get("media_type", None)
                    size = received.get("size", None)
                    url = received.get("url", None)

                    message_data = {
                        "sender_id": str(self._current_sender_relation.id),
                        "conversation_id": str(self._room_id),
                        "type": type,
                        "content": str(data),
                        "name": name,
                        "type": media_type,
                        "size": size,
                        "url": url,
                    }
                else:
                    message_data = {
                        "sender_id": str(self._current_sender_relation.id),
                        "conversation_id": str(self._room_id),
                        "type": type,
                        "content": str(data),
                    }

                if reply and str(reply).strip():
                    message_data["reply"] = str(reply)
                    
                await self._redis_instance.queue_add("message_queue", message_data)
            else:
                await self.exception_send()
        except Exception as e:
            await self.exception_send(e)

    async def disconnect(self, _=None):
        try:
            if self._room_id:
                await self.channel_layer.group_discard(self._room_id, self.channel_name)
        except Exception as e:
            try:
                await self.send(
                    json.dumps(
                        {"message": "connection_error", "data": None},
                        ensure_ascii=False,
                    )
                )
            except Exception as ex:
                raise ex
            LogHelper.error(message=str(e))
