import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

#redis queue auto handle thread 
from channels.routing import ProtocolTypeRouter, URLRouter
import threading
import time
from app.consumers.redisQueueConsumer import RedisQueueConsumer
import app.ws_urls
from app.middlewares.wsJwtMiddleware import WsJwtMiddleware

def redis_queue_auto_thread(queue_key='message_queue'):
    def runner():
        while True:
            try:
                consumer = RedisQueueConsumer(queue_key=queue_key)
                consumer.start()
                while consumer.is_alive():
                    time.sleep(10)
            except Exception:
                time.sleep(10)
    thread = threading.Thread(target=runner, daemon=True)
    thread.start()
if os.environ.get('RUN_MAIN') != 'true':
    redis_queue_auto_thread()

# websocket channel
asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http": asgi_app,
    "websocket": WsJwtMiddleware(
        URLRouter(
            app.ws_urls.websocket_urlpatterns
        )
    )
})
