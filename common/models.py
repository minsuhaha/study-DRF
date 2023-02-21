from django.db import models

class CommonModel(models.Model):
    
    '''Common Model Definition'''

    created = models.DateTimeField(auto_now_add=True) # auto_now_add = True는 처음 만들어 질때만 시간 update해서 설정
    updated = models.DateTimeField(auto_now=True) # auto_now = True는 수정될때마다 시간 update

    # 데이터베이스에 저장하지 않는 모델 설정 / abstract = True
    class Meta: 
        abstract = True