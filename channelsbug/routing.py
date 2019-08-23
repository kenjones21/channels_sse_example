# mysite/routing.py
from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
import app.routing

application = ProtocolTypeRouter({
    "http": URLRouter(
        app.routing.urlpatterns,
    ),
    "websocket": URLRouter(
        app.routing.websocket_urlpatterns
    )
})