from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from apps.testmedia.models import DataModel
from api.admin.testmedia.serializer import MediaDataSerializer

class MediaDataCreateView(CreateAPIView):
    queryset = DataModel.objects.all()
    serializer_class = MediaDataSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(payload=self.request.data)
