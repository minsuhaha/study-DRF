from rest_framework import serializers
from .models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'pk', # 읽기 전용으로 이미 설정 (ModelSerializer에서 기본 설정)
            'file',
            'description',
        )