from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from usrapp.models.models import CustomUser


class UserAdmin(BaseUserAdmin):
    inlines = ()


admin.site.register(CustomUser)
