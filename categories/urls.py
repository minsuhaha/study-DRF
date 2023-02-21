from django.urls import path
from . import views

# class를 가져오기 위해서는 class명칭.as_view() 해줘야함.
urlpatterns = [
    path('', views.CategoryViewSet.as_view(
    { 
        'get' :'list',
        'post' :'create',
    }
    )), 
    path('<int:pk>' , views.CategoryViewSet.as_view(
    {
        'get' : 'retrieve',
        'put' : 'update',
        'delete' : 'destroy',
    }
    )),
]
