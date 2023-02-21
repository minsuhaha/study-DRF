from django.db import models
from users.models import User
from common.models import CommonModel

class Room(CommonModel): # CommonModel 재사용

    """Room Model Definition"""
    
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(max_length=180, default='') # 이미 추가한 방들이 있기에 나중에 들어온 name 필드의 default값 설정해주기
    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80,default="서울")
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(max_length=20,choices=RoomKindChoices.choices)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms',) # related 이름을 설정안해주면 user쪽에서 room 데이터로 접근할때 room_set 을 통해 접근가능!
    amenities = models.ManyToManyField("rooms.Amenity", related_name='rooms',)
    category = models.ForeignKey('categories.Category', null=True, blank=True, on_delete=models.SET_NULL, related_name='rooms',) 

    def __str__(self):
        return self.name

    def total_amenities(self): # amenitity 개수 파악
        return self.amenities.count()

    def rating(self): # 리뷰 평균 점수 파악
        count = self.reviews.count()
        if count == 0:
            return "No Reviews"
        else:
            total_rating = 0
            for review in self.reviews.all().values('rating'): # values 함수 사용함으로써 가져올 데이터를 줄여주기 딕셔너리 형태로 불러옴
                total_rating += review['rating']
            return round(total_rating / count, 1)

class Amenity(CommonModel):

    '''Amenity Definition'''

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name
   
    class Meta:  
        verbose_name_plural = "Amenties" # 모델이름 재설정
