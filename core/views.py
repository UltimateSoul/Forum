from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from core.models import MiniChatMessage, Post, Comment
from core.serializers import MiniChatMessageSerializer, PostSerializer, CommentSerializer
from .models import Topic
from .serializers import TopicSerializer


class TopicView(APIView):
    """Topics"""

    def get(self, request):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


class MiniChatMessagesView(APIView):
    """Mini Chat Messages Get View"""

    def get(self, request):
        mini_chat_messages = MiniChatMessage.objects.all()
        serializer = MiniChatMessageSerializer(mini_chat_messages, many=True)
        return Response(serializer.data)


class PostsView(APIView):
    """Mini Chat Messages Get View"""

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class CommentsView(APIView):
    """Mini Chat Messages Get View"""

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


