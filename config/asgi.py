import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
import app.ws_urls
from app.middlewares.wsJwtMiddleware import WsJwtMiddleware

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
