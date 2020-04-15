from django.contrib import admin

from core.models import UserNotification


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):

    list_display = ('username', 'purpose', 'notification_type', 'message_preview')

    @staticmethod
    def username(obj):
        return obj.user.username

    @staticmethod
    def message_preview(obj):
        return obj.message[:50]