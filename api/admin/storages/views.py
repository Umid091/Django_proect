import os
import requests
from datetime import datetime
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
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
            return Response({"success": False, "detail": "Ro'yxat (list) yuboring"}, status=status.HTTP_400_BAD_REQUEST)

        BASE_HOST = "https://dev.ohayo.uz/media/"
        instances_to_create = []
        results = []
        errors = []

        for item in data_list:
            raw_url = str(item.get("recording", "")).strip()
            clean_url = raw_url.replace("https:recordings/", "recordings/").replace("http:recordings/", "recordings/")
            full_url = clean_url if clean_url.startswith("http") else BASE_HOST + clean_url

            try:
                response = requests.get(full_url, timeout=20)
                if response.status_code == 200:
                    filename = os.path.basename(full_url.split('?')[0])
                    date_path = datetime.now().strftime("recordings/%Y/%m/%d")
                    save_path = os.path.join(date_path, filename)

                    saved_path = default_storage.save(save_path, ContentFile(response.content))

                    instances_to_create.append(Storages(
                        recording=saved_path,
                        media_id=item.get("media_id"),
                        solution_id=item.get("solution_id"),
                        report_id=item.get("report_id"),
                        type=item.get("type", "part")
                    ))
                else:
                    errors.append({"url": full_url, "error": f"Status {response.status_code}"})
            except Exception as e:
                errors.append({"url": full_url, "error": str(e)})

        if instances_to_create:
            created_instances = Storages.objects.bulk_create(instances_to_create,   batch_size=1000)
            for inst in created_instances:
                results.append({
                    "id": inst.id,
                    "media_id": inst.media_id,
                    "recording": str(inst.recording),
                    "type": inst.type
                })

        if instances_to_create and not errors:
            return Response({
                "success": True,
                "message": f"{len(results)} ta fayl muvaffaqiyatli saqlandi.",
                "results": results
            }, status=status.HTTP_201_CREATED)

        elif instances_to_create and errors:
            return Response({
                "success": False,
                "message": f"Qisman bajarildi: {len(results)} ta saqlandi, {len(errors)} ta xatolik bor.",
                "results": results,
                "errors": errors
            }, status=status.HTTP_207_MULTI_STATUS)

        else:
            return Response({
                "success": False,
                "message": "Hech qaysi fayl saqlanmadi.",
                "errors": errors
            }, status=status.HTTP_400_BAD_REQUEST)