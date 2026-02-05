import asyncio
import threading
import json
import time
from channels.layers import get_channel_layer
from app.infrastructures.redis.redisClient import RedisClient
from app.mapping.mediaMapping import MediaMapping
from app.mapping.messageMapping import MessageMapping
from app.mapping.profileMapping import ProfileMapping
from app.utils.logHelper import LogHelper
from app.services.messageService import MessageService
from app.enums.messageTypes import MessageTypes
from app.services.mediaService import MediaService
from asgiref.sync import sync_to_async


class RedisQueueWorker:
    def __init__(self, queue_key="message_queue"):
        self.queue_key = queue_key
        self.running = True

    async def run(self):
        redis = (await RedisClient.instance()).client
        channel_layer = get_channel_layer()

        while self.running:
            try:
                result = await redis.blpop(self.queue_key, timeout=5)
                if not result:
                    continue

                _, data_str = result
                data = json.loads(data_str)

                if data["type"] == MessageTypes.TEXT:
                    await self.text_message_handler(data, channel_layer)
                elif data["type"] == MessageTypes.MEDIA:
                    await self.media_message_handler(data, channel_layer)

            except Exception as e:
                LogHelper.error(message=str(e))
                await asyncio.sleep(1)


    async def text_message_handler(self, data):
        try:
            result = await sync_to_async(MessageService.create)(data=data)

            if result:
                channel_layer = get_channel_layer()
                await channel_layer.group_send(
                    str(result.conversation.id),
                    {
                        "type": MessageTypes.TEXT,
                        "content": json.loads(json.dumps(MessageMapping(result).data, default=str)),
                        "sender": json.loads(json.dumps(ProfileMapping(result.sender.profile).data, default=str)),
                        "reply": str(result.reply) if result.reply else None
                    },
                )
        except Exception as e:
            LogHelper.error(message=str(e))

    async def media_message_handler(self, data):
        try:
            media_created = await MediaService.create(data=data)

            if media_created:
                data["media_id"] = media_created.id
                result = await MessageService.create(data=data)

                if result:
                    channel_layer = get_channel_layer()
                    await channel_layer.group_send(
                        str(result.conversation.id),
                        {
                            "type": MessageTypes.MEDIA,
                            "content": json.loads(json.dumps(MessageMapping(result).data, default=str)),
                            "sender": json.loads(json.dumps(ProfileMapping(result.sender.profile).data, default=str)),
                            "media": json.loads(json.dumps(MediaMapping(result.media).data, default=str)),
                            "reply": (
                                str(result.reply) if result.reply else None
                            ),
                        },
                    )
        except Exception as e:
            LogHelper.error(message=str(e))