from rest_framework import serializers
from apps.testmedia.models import DataModel

class MediaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataModel
        fields = ['payload']