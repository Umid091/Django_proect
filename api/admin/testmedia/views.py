from rest_framework.generics import CreateAPIView
from apps.testmedia.models import DataModel
from api.admin.testmedia.serializer import MediaDataSerializer

class MediaDataCreateView(CreateAPIView):
    queryset = DataModel.objects.all()
    serializer_class = MediaDataSerializer

    def perform_create(self, serializer):
        serializer.save(payload=self.request.data)