from django.contrib import admin

from api.models import MiniChatMessage, Topic, Comment, Post, Like


# Register your models here.


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'preview')

    @staticmethod
    def preview(obj):
        return obj.body[:40]


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


@admin.register(Like)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'post', 'created_at')
