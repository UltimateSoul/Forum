from django.contrib import admin
from .models import Topic
# Register your models here.


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'preview')

    @staticmethod
    def preview(obj):
        return obj.body[:40]
