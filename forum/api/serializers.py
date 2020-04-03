from rest_framework import serializers
from django.contrib.auth import get_user_model
from api import services
from api.models import MiniChatMessage, Topic, Post, Comment
from users.serializers import RestrictedUserSerializer, UserSerializer

User = get_user_model()


class TopicSerializer(serializers.ModelSerializer):
    """Topic Serializer"""
    author = UserSerializer()
    posts_quantity = serializers.ReadOnlyField()
    total_likes = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Topic
        fields = '__all__'

    def validate_body(self, value):
        if not value:
            raise serializers.ValidationError("Text body is empty!")

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is empty!")

    def get_is_liked(self, obj) -> bool:
        """Checks if user have already liked object or not"""

        user = self.context.get('request').user
        return services.is_liked(obj, user)


class CreateTopicSerializer(serializers.ModelSerializer):
    """Create Topic Serializer"""
    author = RestrictedUserSerializer(required=False)

    class Meta:
        model = Topic
        fields = ['title', 'author', 'body', 'icon', 'description', 'section', 'id']


class EditTopicSerializer(serializers.ModelSerializer):
    """Create Topic Serializer"""
    author = RestrictedUserSerializer(required=False)

    class Meta:
        model = Topic
        fields = ['author', 'body', 'icon', 'description', 'section']


class MiniChatMessageSerializer(serializers.ModelSerializer):
    """Home page minichat messages"""
    author = RestrictedUserSerializer()

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
    author = RestrictedUserSerializer(required=False)
    comments = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    total_likes = serializers.ReadOnlyField()

    def get_is_liked(self, obj) -> bool:
        """Checks if user have already liked object or not"""

        user = self.context.get('request').user
        return services.is_liked(obj, user)

    def get_comments(self, post):
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': self.context.get('request')})
        return serializer.data

    class Meta:
        model = Post
        fields = ['topic',
                  'is_liked',
                  'author',
                  'total_likes',
                  'body',
                  'created_at',
                  'edited_at',
                  'comments',
                  'id']


class CommentSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""
    author = RestrictedUserSerializer(required=False)
    is_liked = serializers.SerializerMethodField()
    total_likes = serializers.ReadOnlyField()


    def get_is_liked(self, obj) -> bool:
        """Checks if user have already liked object or not"""

        user = self.context.get('request').user
        return services.is_liked(obj, user)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'body',
            'total_likes',
            'is_liked',
            'created_at',
            'edited_at'
        ]


class FanSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'avatar',
            'username',
            'game_nickname',
        )