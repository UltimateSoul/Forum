from rest_framework import serializers

from core.models import MiniChatMessage, Topic, Post, Comment
from users.serializers import UserSerializer


class TopicSerializer(serializers.ModelSerializer):
    """Topic Serializer"""
    author = UserSerializer()

    class Meta:
        model = Topic
        fields = '__all__'


class MiniChatMessageSerializer(serializers.ModelSerializer):
    """Home page minichat messages"""
    author = UserSerializer()

    class Meta:
        model = MiniChatMessage
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""
    author = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
