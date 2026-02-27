from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username','user_type')


# admin.site.register(CustomUser)