from django.contrib import admin

from core.models import MiniChatMessage, Post, Comment
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'game_nickname', 'date_joined')

    @staticmethod
    def full_name(obj):
        return obj.first_name + " " + obj.last_name


@admin.register(MiniChatMessage)
class MiniChatMessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'created_date')

    @staticmethod
    def body(obj):
        return obj.body[:35]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('topic', 'body', 'author')

    @staticmethod
    def body(obj):
        return obj.body[:35]

    @staticmethod
    def topic(obj):
        return obj.post.topic.title


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'body', 'author', 'published_date')

    @staticmethod
    def body(obj):
        return obj.body[:35]

    @staticmethod
    def topic(obj):
        return obj.topic.title
