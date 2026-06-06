from calendar import day_abbr

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.testmedia.models import DataModel
from rest_framework.views import APIView

# from api.admin.testmedia.serializer import MediaDataSerializer

class MediaDataCreateView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        data =request.data
        obj=DataModel.objects.create(payload=data)

        return Response(
            {
                'key':data
            }
        )




