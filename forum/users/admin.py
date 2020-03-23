from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('game_nickname',
                    'email',
                    'popularity',
                    'blood_coins',
                    'date_joined')



