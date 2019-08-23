# chat/routing.py
from django.conf.urls import url

from . import consumers, views
from channels.http import AsgiHandler

urlpatterns = [
    url('test', consumers.ServerSentEventsConsumer),
    url(r'', AsgiHandler)
]

websocket_urlpatterns = [
    url('ws', consumers.ChatConsumer)
]