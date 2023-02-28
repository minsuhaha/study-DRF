from django.db import models
from common.models import CommonModel

class Photo(CommonModel):

    file = models.URLField()
    description = models.CharField(max_length=140,)
    room = models.ForeignKey('rooms.Room', null=True, blank=True, on_delete=models.CASCADE, related_name='photos')
    experience = models.ForeignKey('experiences.Experience', null=True, blank=True, on_delete=models.CASCADE, related_name='photos')

    def __str__(self) -> str:
        return "Photo file"

class Viedo(CommonModel):
    
    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience", on_delete=models.CASCADE, related_name='viedos',
    ) # experience도 동영상 한개, 동영상에도 experience 한개만 연결가능!

    def __str__(self) -> str:
        return "Video file"