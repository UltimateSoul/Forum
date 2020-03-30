from django.http import JsonResponse
from django.views.generic import TemplateView
from requests import request
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet, ViewSet

from api.helpers import status as tbw_status
from api.models import MiniChatMessage, Post, Comment, Like
from api.serializers import MiniChatMessageSerializer, PostSerializer, CommentSerializer, \
    CreateTopicSerializer, CreateMiniChatMessageSerializer, EditTopicSerializer
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, RegisterUserSerializer, RestrictedUserSerializer, UserProfileSerializer
from .helpers.permissions import check_ability_to_edit, check_ability_to_delete
from .mixins import LikedMixin
from .models import Topic
from .serializers import TopicSerializer

User = get_user_model()


class HomeView(TemplateView):
    template_name = 'home.html'


class TopicViewSet(ModelViewSet, LikedMixin):
    paginator = LimitOffsetPagination()
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

    def get_object(self):
        topic_id = self.kwargs.get('topic_id')
        queryset = Topic.objects.all()
        obj = get_object_or_404(queryset, id=topic_id)
        return obj

    def list(self, request, *args, **kwargs):
        topics = Topic.objects.all()
        queryset = self.paginator.paginate_queryset(topics, request)
        serializer = TopicSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CreateTopicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        topic = serializer.save(author=self.request.user)
        return Response(status=status.HTTP_201_CREATED, data={'topic_id': topic.id})

    def retrieve(self, request, *args, **kwargs):
        topic = self.get_object()
        serializer = TopicSerializer(topic, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        topic = self.get_object()
        is_able_to_edit = check_ability_to_edit(user=self.request.user, obj=topic)
        if is_able_to_edit:
            serializer = EditTopicSerializer(topic, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK, data={'topic_id': topic.id})
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        topic = self.get_object()
        is_able_to_delete = check_ability_to_delete(user=self.request.user)
        if is_able_to_delete:
            topic.delete()
            return Response()
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['GET'], detail=False)
    def search(self, request, *args, **kwargs):
        search_data = request.GET
        section = kwargs['section'].upper()
        search_by = search_data['searchBy']
        if search_by == 'title':
            topic_exists = Topic.objects.filter(title=search_data['value'],
                                                section=section).exists()
            return Response(data={'topic_exists': topic_exists})
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def topics_by_section(self, request, *args, **kwargs):
        section = kwargs.get('section')
        topics = Topic.objects.filter(section=section.upper())
        queryset = self.paginator.paginate_queryset(topics, request)
        serializer = TopicSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class PostsViewSet(ModelViewSet, LikedMixin):
    """Mini Chat Messages Get View"""

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    # Add additional permission, posts can write only users with checked email

    def get_queryset(self):
        if self.request.GET.get('topic'):
            return self.queryset.filter(topic=self.request.GET.get('topic'))
        return self.queryset

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(ModelViewSet, LikedMixin):
    """Mini Chat Messages Get View"""

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    # Add additional permission, posts can write only users with checked email

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserProfileView(APIView):
    """User Profile View"""

    @staticmethod
    def get(request, *args, **kwargs):
        user_id = kwargs.get('id')
        is_main_user = request.user.id == user_id
        try:
            user = User.objects.get(id=user_id)  # ToDo: add handling exception if user doesn't exists and write tests
            if is_main_user:
                serializer = UserSerializer(user)
            else:
                serializer = RestrictedUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist as error:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': str(error)})

    def patch(self, request, *args, **kwargs):
        """Here user can change his profile data"""
        user_id = kwargs.get('id')
        user = request.user
        is_main_user = user.id == user_id or user.is_staff or user.is_superuser
        if is_main_user:  # checks if it`s owner of profile
            serializer = UserProfileSerializer(user, data=request.data)
            if serializer.is_valid():
                user.prepare_to_save()
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': 'Cheater!'})


class GetUserView(APIView):
    """Fetch user view"""

    @staticmethod
    def get(request, *args, **kwargs):
        token = Token.objects.get(key=request.GET.get('auth_token'))
        user = User.objects.get(auth_token=token)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UsersView(APIView):
    """All Users View"""

    @staticmethod
    def get(request, *args, **kwargs):
        if request.GET.get('email'):
            # Uses in registration process. Checks if email is unique
            users = User.objects.filter(email=request.GET.get('email'))
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        elif request.GET.get('username'):
            users = User.objects.filter(username=request.GET.get('username'))
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        user_serializer = RegisterUserSerializer(data=data)
        if user_serializer.is_valid():
            user = User.objects.create_user(
                **user_serializer.data
            )
            # settings.BASE_DIR  ToDo: add default image (situated in static folder)
            token = Token.objects.get(user=user)
            return JsonResponse(data={'auth_token': token.key})
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': user_serializer.errors})
