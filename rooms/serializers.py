from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description",)


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('pk', 'name', 'country', 'city', 'price',)


class RoomDetailSerializer(serializers.ModelSerializer):
    # 이런식으로 사용하려면 무조건 foreign key로 연결되어있어야 함.
    owner = TinyUserSerializer(read_only=True) # DRF Serializer에서 owner(Room모델안에 있는)를 가지고 올때 TinyUserSerializer에서 데이터를 가져옴
    amenities = AmenitySerializer(read_only = True, many=True) # 여러개있을땐 many=True 꼭!!
    category = CategorySerializer(read_only = True)

    class Meta:
        model = Room
        fields = "__all__"


