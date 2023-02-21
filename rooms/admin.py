from django.contrib import admin
from .models import Room, Amenity

@admin.action(description="Set all prices to zero") # admin.action 은 3개의 매개변수(model_admin, request(액션을 호출한 유저정보), queryset) 를 호출함.
def reset_prices(model_admin, request, rooms):
    for room in rooms:
        room.price = 0
        room.save()

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)
    list_display = (
        'name',
        'price',
        'kind',
        'total_amenities',
        'rating',
        'owner',
        'created',
   
    )

    list_filter = (
        'country',
        'city',
        'pet_friendly',
        'kind',
        'amenities',
        'created',
        'updated',
    )
    # foreign key 설정을 한 필드는 __ 를 통해 해당 모델로 연결
    search_fields = (
        'owner__username', # 기본적으로 contains 사용
    )

    # def total_amenities(self,room):
    #     return room.amenities.count()

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'created',
        'updated',
    )
    
    # 모델안에 없는 field 세부사항 admin에 보여지도록 추가
    readonly_fields = (
        'created',
        'updated',
    )
