from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'game_nickname', 'date_joined')

    @staticmethod
    def full_name(obj):
        return obj.first_name + " " + obj.last_name
