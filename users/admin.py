from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # fielidsets -> admin 상세페이지
    fieldsets = (
    ("Profile", 
        {
            "fields": ('avatar','username','password','name','email','is_host','gender','language','curreny'),
        },
    ),       
    ("Permission",
        {
            "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            # "classes": ("collapse",)
        },
        
    ),
    ("Important Date",
        {
            "fields": ("last_login", "date_joined"),
            # "classes" : ("collapse",)
        },
    ),
    )

    list_display = ("username", "email", "name", "is_host") # admin 메인화면에 보이는 column