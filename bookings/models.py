from django.db import models
from common.models import CommonModel

class Booking(CommonModel):

    ''' Booking Model Definition '''

    class BookingKindChoices(models.TextChoices):
        ROOM = 'room', 'Room'
        EXPERIENCE = 'experience', 'Experience'

    kind = models.CharField(max_length=15, choices=BookingKindChoices.choices,)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey('rooms.Room', null=True, blank=True, on_delete=models.SET_NULL, related_name='bookings')
    experience = models.ForeignKey('experiences.Experience', null=True, blank=True, on_delete=models.SET_NULL, related_name='bookings')
    check_in = models.DateField(null=True, blank=True,) # 유저가 experience를 예약하기도 하니 check_in or out 시간이 없을수도 있다!
    check_out = models.DateField(null=True, blank=True,)
    experience_time = models.DateTimeField(null=True, blank=True,) # 유저가 room을 예약할 경우 experence_time이 필요없다!
    guests = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.kind.title()} booking for : {self.user}'
        # kind는 문자열이나 title() 함수 사용 가능!