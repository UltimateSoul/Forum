from rest_framework import serializers

from api.models import MiniChatMessage, Topic, Post, Comment, Like
from users.serializers import RestrictedUserSerializer


class TopicSerializer(serializers.ModelSerializer):
    """Topic Serializer"""
    author = RestrictedUserSerializer()

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
    likes = serializers.SerializerMethodField()

    def get_comments(self, post):
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_likes(self, post):
        likes = post.post_likes.all().count()
        return likes

    class Meta:
        model = Post
        fields = ['topic',
                  'likes',
                  'author',
                  'body',
                  'published_date',
                  'edited_date',
                  'comments',
                  'id']


class CreatePostSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""

    class Meta:
        model = Post
        fields = ['topic', 'body']


class CommentSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""
    author = RestrictedUserSerializer()
    likes = serializers.SerializerMethodField()

    def get_likes(self, comment):
        likes = comment.comment_likes.all().count()
        return likes

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'body',
            'likes',
            'published_date'
        ]


class CreateCommentSerializer(serializers.ModelSerializer):
    """Topic's post serializer"""

    class Meta:
        model = Comment
        fields = ['post', 'body']


class CreateLikeSerializer(serializers.ModelSerializer):
    """Create likes serializer"""

    class Meta:
        model = Like
        fields = ['post', 'comment', 'user']