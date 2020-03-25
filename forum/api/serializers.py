from rest_framework import serializers

from api.models import MiniChatMessage, Topic, Post, Comment
from users.serializers import RestrictedUserSerializer


class TopicSerializer(serializers.ModelSerializer):
    """Topic Serializer"""
    author = RestrictedUserSerializer()
    posts_quantity = serializers.SerializerMethodField()

    def get_posts_quantity(self, topic):
        return Post.objects.filter(topic=topic).count()

    class Meta:
        model = Topic
        fields = '__all__'

    def validate_body(self, value):
        if not value:
            raise serializers.ValidationError("Text body is empty!")

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is empty!")


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
    author = RestrictedUserSerializer()
    topic = TopicSerializer()
    comments = serializers.SerializerMethodField()

    def get_comments(self, post):
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    class Meta:
        model = Post
        fields = ['topic', 'author', 'body', 'rating', 'published_date', 'edited_date', 'comments', 'id']


class CreatePostSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""

    class Meta:
        model = Post
        fields = ['topic', 'body']


class CommentSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""
    author = RestrictedUserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CreateCommentSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""

    class Meta:
        model = Comment
        fields = ['post', 'body']
