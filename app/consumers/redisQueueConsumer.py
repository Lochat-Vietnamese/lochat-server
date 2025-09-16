import threading
import json
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from app.mapping.mediaMapping import MediaMapping
from app.mapping.messageMapping import MessageMapping
from app.mapping.profileMapping import ProfileMapping
from app.utils.logHelper import LogHelper
from app.utils.redisClient import RedisClient
from app.services.messageService import MessageService
from app.enums.messageTypes import MessageTypes
from app.services.mediaService import MediaService


class RedisQueueConsumer(threading.Thread):
    def __init__(self, queue_key="message_queue"):
        super().__init__(daemon=True)
        self.queue_key = queue_key
        self.running = True
        redis_instance = async_to_sync(RedisClient.instance)()
        self.redis = redis_instance.client

    def run(self):
        while self.running:
            try:
                result = self.redis.blpop(self.queue_key, timeout=5)
                if result:
                    _, data_str = result
                    data = json.loads(data_str)
                    if data.get("type") == MessageTypes.TEXT:
                        async_to_sync(self.text_message_handler)(data)
                    elif data.get("type") == MessageTypes.MEDIA:
                        async_to_sync(self.media_message_handler)(data)
            except Exception as e:
                LogHelper.error(message=str(e))
                time.sleep(1)
                
    def stop(self):
        self.running = False


    async def text_message_handler(self, data):
        try:
            result = await MessageService.create(data=data)

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