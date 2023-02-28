from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description",)


class RoomListSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField() # rating 값을 계산할 method를 만들거임.
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ('pk', 'name', 'country', 'city', 'price','rating','photos')

    def get_rating(self, room): #SerializerMethodField 를 사용하면 꼭 get_변수이름 이름 함수를 지정해줘야 함.
        return room.rating()

class RoomDetailSerializer(serializers.ModelSerializer):
    # 이런식으로 사용하려면 무조건 foreign key로 연결되어있어야 함.
    owner = TinyUserSerializer(read_only=True) # DRF Serializer에서 owner(Room모델안에 있는)를 가지고 올때 TinyUserSerializer에서 데이터를 가져옴
    amenities = AmenitySerializer(read_only = True, many=True) # 여러개있을땐 many=True 꼭!!
    category = CategorySerializer(read_only = True)
    rating = serializers.SerializerMethodField() # rating 값을 계산할 method를 만들거임.
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)
    # reviews = ReviewSerializer(many=True, read_only=True) # related_name으로 필드명 설정해줘야 작동, 역접근자(역참조) -> room.reviews

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room): #SerializerMethodField 를 사용하면 꼭 get_변수이름 이름 함수를 지정해줘야 함.
        return room.rating()
    
    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user # room 소유자와 요청한 유저가 같은 사람이면 true, 아니면 false 반환
