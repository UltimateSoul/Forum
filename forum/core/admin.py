from django.contrib import admin

from core.models import UserNotification, ModeratorLog


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):

    list_display = ('username', 'purpose', 'notification_type', 'message_preview')

    @staticmethod
    def username(obj):
        return obj.user.username

    @staticmethod
    def message_preview(obj):
        return obj.message[:50]


@admin.register(ModeratorLog)
class ModeratorLogAdmin(admin.ModelAdmin):

    list_display = ('moderator', 'action_preview', 'created_at')

    @staticmethod
    def moderator(obj):
        return obj.user.username

    @staticmethod
    def action_preview(obj):
        return obj.action[:50]
