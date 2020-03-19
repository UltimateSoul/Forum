from rest_framework import serializers

from api.models import MiniChatMessage, Topic, Post, Comment
from users.serializers import UserSerializer


class TopicSerializer(serializers.ModelSerializer):
    """Topic Serializer"""
    author = UserSerializer()
    posts_quantity = serializers.SerializerMethodField()

    def get_posts_quantity(self, topic):
        return Post.objects.filter(topic=topic).count()

    class Meta:
        model = Topic
        fields = '__all__'


class CreateTopicSerializer(serializers.ModelSerializer):
    """Create Topic Serializer"""

    class Meta:
        model = Topic
        fields = ['title', 'body', 'icon', 'description', 'section']


class MiniChatMessageSerializer(serializers.ModelSerializer):
    """Home page minichat messages"""
    author = UserSerializer()

    class Meta:
        model = MiniChatMessage
        fields = '__all__'


class CreateMiniChatMessageSerializer(serializers.ModelSerializer):
    """Home page minichat messages"""

    class Meta:
        model = MiniChatMessage
        fields = ['body']


class PostSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""
    author = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class CreatePostSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""

    class Meta:
        model = Post
        fields = ['topic', 'body']


class CommentSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CreateCommentSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""

    class Meta:
        model = Comment
        fields = ['post', 'body']
