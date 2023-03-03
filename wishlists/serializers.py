from rest_framework import serializers
from rooms.serializers import RoomListSerializer
from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    
    rooms = RoomListSerializer(many=True, read_only=True) # 유저가 방에 대한 정보를 보내기를 원하지 않기에 read_only = True

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )