from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/gallery/$', consumers.GalleryConsumer.as_asgi()),
]