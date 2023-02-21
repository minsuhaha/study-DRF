from django.contrib import admin
from .models import Review

class WordFilter(admin.SimpleListFilter): # 필터 추가 class

    title = 'Filter by word!' # filter 제목

    parameter_name = 'word' # url에 나타나는 이름 ex) potato = good 형식으로 url에 찍힘

    def lookups(self, request, model_admin): # 필터 look up
        return [
            ('good', 'Good'),
            ('great', 'Great'),
            ('awesome', 'Awesome'),
        ]
    
    def queryset(self, request, reviews): #reviews는 queryset임
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    
    list_display = (
        '__str__',
        'payload',
    )

    list_filter = (WordFilter, 'rating', "user__is_host", "room__category",)