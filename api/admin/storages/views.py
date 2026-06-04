
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from apps.storages.models import Storages


class StoragesListCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Storages.objects.all().values(
            'id', 'recording', 'media_id', 'solution_id', 'report_id', 'type'
        )

        return Response({
            "success": True,
            "count": queryset.count(),
            "results": list(queryset)
        }, status=status.HTTP_200_OK)

    def post(self, request):
        data_list = request.data

        if not isinstance(data_list, list):
            return Response({
                "success": False,
                "detail": "Ma'lumotlar JSON ro'yxat (massiv) ko'rinishida bo'lishi shart"
            }, status=status.HTTP_400_BAD_REQUEST)

        storage_objects = []

        for item in data_list:
            media_id = item.get('media_id')
            solution_id = item.get('solution_id')
            report_id = item.get('report_id')

            obj = Storages(
                recording=item.get('recording'),
                media_id=int(media_id) if media_id else None,
                solution_id=int(solution_id) if solution_id else None,
                report_id=int(report_id) if report_id else None,
                type=item.get('type', 'part')
            )
            storage_objects.append(obj)

        if not storage_objects:
            return Response({
                "success": False,
                "detail": "Yuborilgan ro'yxat bo'sh"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            created_instances = Storages.objects.bulk_create(storage_objects, batch_size=1000) ###bu batch_size malumotlarni 1000 talab oladi mingtadan ko'p bo'lsa.

            response_data = []
            for instance in created_instances:
                response_data.append({
                    "id": instance.id,
                    "recording": instance.recording.url if instance.recording else None,
                    "media_id": instance.media_id,
                    "solution_id": instance.solution_id,
                    "report_id": instance.report_id,
                    "type": instance.type
                })

            return Response({
                "success": True,
                "message": f" Jami {len(response_data)} ta ma'lumot muvaffaqiyatli saqlandi ",
                "results": response_data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "success": False,
                "detail": f"  bazaga yozishda xatolik chiqdi: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)