from django.urls import path
from api.admin.testmedia.views import MediaDataCreateView
urlpatterns = [
    path('upload/', MediaDataCreateView.as_view(), name='media-upload'),
]