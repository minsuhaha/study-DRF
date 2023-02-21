from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")  # (value(데이터베이스에 들어가는 값), label(화면에 보이는 값))
        FEMALE = ('female','Female')

    class LanguageChoices(models.TextChoices):
        KR = ('kr', 'Korea')
        EN = ('en', 'English')

    class CurrencyChoices(models.TextChoices):
        WON = ('won', 'Korean Won')
        USD = ('usd','Dollar')

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    avatar = models.ImageField(blank=True) # blank = True -> form에서 필드가 필수적이지 않게 해줌 / null=True는 데이터베이스에서 필드가 null 값을 가질 수 있게 해주는거라 다름
    name = models.CharField(max_length=150, default='')
    is_host = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices)
    curreny = models.CharField(max_length=5,choices=CurrencyChoices.choices)