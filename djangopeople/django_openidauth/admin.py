from django.contrib import admin

from .models import UserOpenID


@admin.register(UserOpenID)
class UserOpenIDAdmin(admin.ModelAdmin):
    pass
