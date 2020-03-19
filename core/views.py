from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from core.models import MiniChatMessage, Post, Comment
from core.serializers import MiniChatMessageSerializer, PostSerializer, CommentSerializer, CreateCommentSerializer, \
    CreateTopicSerializer, CreateMiniChatMessageSerializer, CreatePostSerializer
from users.models import User
from users.serializers import UserSerializer
from .models import Topic
from .serializers import TopicSerializer


class HomeView(TemplateView):
    template_name = 'home.html'


class TopicView(APIView):
    """Topics"""

    @staticmethod
    def get(request):
        section = request.GET.get('section')
        if section:
            topics = Topic.objects.filter(section=request.GET.get('section'))
            serializer = TopicSerializer(topics, many=True)
            return Response(serializer.data)
        else:
            topics = Topic.objects.all()
            serializer = TopicSerializer(topics, many=True)
            return Response(serializer.data)

    def post(self, request):
        topic = CreateTopicSerializer(data=request.data)
        if topic.is_valid():
            topic.save(author=request.user)
            return Response({'success': True})
        else:
            return Response({'success': False,
                             'errors': topic.error_messages})


class MiniChatMessagesView(APIView):
    """Mini Chat Messages Get View"""

    @staticmethod
    def get(request):
        mini_chat_messages = MiniChatMessage.objects.all()
        serializer = MiniChatMessageSerializer(mini_chat_messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        mini_chat_message = CreateMiniChatMessageSerializer(data=request.data)
        if mini_chat_message.is_valid():
            mini_chat_message.save(author=request.user)
            return Response({'success': True})
        else:
            return Response({'success': False,
                             'errors': mini_chat_message.error_messages})


class PostsView(APIView):
    """Mini Chat Messages Get View"""

    @staticmethod
    def get(request):
        topic = request.GET.get('topic')
        posts = Post.objects.filter(topic=topic)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        post = CreatePostSerializer(data=request.data)
        if post.is_valid():
            post.save(author=request.user)
            return Response({'success': True})
        else:
            return Response({'success': False,
                             'errors': post.error_messages})


class CommentsView(APIView):
    """Mini Chat Messages Get View"""

    @staticmethod
    def get(request):
        post = request.GET.get('post')
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        comment = CreateCommentSerializer(data=request.data)
        if comment.is_valid():
            comment.save(author=request.user)
            return Response({'success': True})
        else:
            return Response({'success': False,
                             'errors': comment.error_messages})


class UserProfileView(APIView):
    """User Profile View"""

    @staticmethod
    def get(request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.filter(id=user_id)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class GetUserView(APIView):
    """Fetch user view"""

    @staticmethod
    def get(request, *args, **kwargs):
        token = Token.objects.get(key=request.GET.get('auth_token'))
        user = User.objects.filter(auth_token=token)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class UsersView(APIView):
    """All Users View"""

    @staticmethod
    def get(request, *args, **kwargs):
        if request.GET:
            # Uses in registration process. Checks if email is unique
            users = User.objects.filter(email=request.GET.get('email'))
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)


class RegistrationView(APIView):

    permission_classes = [AllowAny]

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        if not User.objects.filter(email=request.GET.get('email')):
            user = User.objects.create_user(
                username=data['username'],
                gender=data['gender'],
                game_nickname=data['gameNickName'],
                email=data['email'],
                password=data['password']
            )
            token = Token.objects.get(user=user)
            return JsonResponse(data={'auth_token': token.key})
        else:
            return JsonResponse(data={'auth_token': False,
                                      'error': 'User with this email already exists!'})