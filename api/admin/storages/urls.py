from django.urls import path
from .views import StoragesListCreateAPIView

urlpatterns = [
    path('recordings/', StoragesListCreateAPIView.as_view(), name='storages_list_create'),
]