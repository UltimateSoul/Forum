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
from api.serializers import MiniChatMessageSerializer, PostSerializer, CommentSerializer, CreateCommentSerializer, \
    CreateTopicSerializer, CreateMiniChatMessageSerializer, CreatePostSerializer, EditTopicSerializer, \
    CreateLikeSerializer
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, RegisterUserSerializer, RestrictedUserSerializer, UserProfileSerializer
from .helpers.permissions import check_ability_to_edit, check_ability_to_delete
from .models import Topic
from .serializers import TopicSerializer

User = get_user_model()


class HomeView(TemplateView):
    template_name = 'home.html'


class TopicView(APIView):
    """Topics"""
    paginator = LimitOffsetPagination()

    def get(self, request):
        section = request.GET.get('section')
        if request.GET.get('searchBy'):
            return self.search_logic()
        if section:
            topics = Topic.objects.filter(section=section)
            page_results = self.paginator.paginate_queryset(topics, request)
            serializer = TopicSerializer(page_results, many=True)
            return Response(serializer.data)
        topics = Topic.objects.all()
        page_results = self.paginator.paginate_queryset(topics, request)
        serializer = TopicSerializer(page_results, many=True)
        return Response(serializer.data)

    def post(self, request):
        topic = CreateTopicSerializer(data=request.data)
        if topic.is_valid():
            topic = topic.save(author=request.user)
            return Response({'success': True,
                             'topic_id': topic.id},
                            status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'success': False,
                              'errors': topic.error_messages})

    def patch(self, request, *args, **kwargs):
        try:
            topic = Topic.objects.get(id=request.data.get('id'))
            serializer = EditTopicSerializer(topic, data=request.data)
            if serializer.is_valid():
                topic = serializer.save()
                return Response({'success': True,
                                 'topic_id': topic.id},
                                status=status.HTTP_200_OK)
            else:
                return Response({'success': False,
                                 'errors': topic.error_messages})
        except Topic.DoesNotExist as error:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': str(error)})

    def search_logic(self):
        search_data = self.request.GET
        search_by = search_data['searchBy']
        if search_by == 'title':
            topic_exists = Topic.objects.filter(title=search_data['value'],
                                                section=search_data['section']).exists()
            return Response(data={'topic_exists': topic_exists})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TopicViewSet(ViewSet):
    paginator = LimitOffsetPagination()

    def list(self, request):
        topics = Topic.objects.all()
        queryset = self.paginator.paginate_queryset(topics, request)
        serializer = TopicSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CreateTopicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        topic_id = kwargs.get('topic_id')
        topic = Topic.objects.get(id=topic_id)
        serializer = TopicSerializer(topic)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        topic_id = kwargs.get('topic_id')
        topic = Topic.objects.get(id=topic_id)
        is_able_to_edit = check_ability_to_edit(user=self.request.user, obj=topic)
        if is_able_to_edit:
            serializer = EditTopicSerializer(topic, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, *args, **kwargs):
        topic_id = kwargs.get('topic_id')
        topic = Topic.objects.get(id=topic_id)
        is_able_to_delete = check_ability_to_delete(user=self.request.user)
        if is_able_to_delete:
            topic.delete()
            return Response()
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['GET'], detail=False)
    def search(self, request, *args, **kwargs):
        search_data = request.GET
        search_by = search_data['searchBy']
        if search_by == 'title':
            topic_exists = Topic.objects.filter(title=search_data['value'],
                                                section=kwargs['section']).exists()
            return Response(data={'topic_exists': topic_exists})
        return Response(status=status.HTTP_400_BAD_REQUEST)  # ToDo sync in front part

    @action(methods=['GET'], detail=False)
    def topics_by_section(self, request, *args, **kwargs):
        section = kwargs.get('section')
        topics = Topic.objects.filter(section=section.upper())
        queryset = self.paginator.paginate_queryset(topics, request)
        serializer = TopicSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTopicView(APIView):
    """Get topic by id"""

    def get(self, request, *args, **kwargs):
        topic_id = kwargs.get('topic_id')
        if topic_id:
            topic = Topic.objects.get(id=topic_id)
            topic = TopicSerializer(topic)
            return Response(data=topic.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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

    paginator = LimitOffsetPagination()

    def get(self, request):
        topic = request.GET.get('topic')
        posts = Post.objects.filter(topic=topic)
        page_results = self.paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(page_results, many=True)
        return Response(serializer.data)

    def post(self, request):
        post = CreatePostSerializer(data=request.data)
        if post.is_valid():
            post.save(author=request.user)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False,
                             'errors': post.error_messages},
                            status=status.HTTP_400_BAD_REQUEST)


class CommentsView(APIView):
    """Mini Chat Messages Get View"""

    @staticmethod
    def get(request):
        post = request.GET.get('post')
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        comment = CreateCommentSerializer(data=request.data)
        if comment.is_valid():
            comment.save(author=request.user)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False,
                             'errors': comment.error_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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
        is_main_user = request.user.id == user_id
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


class LikesView(APIView):
    """LikesView"""

    def post(self, request, *args, **kwargs):
        serializer = CreateLikeSerializer(data=request.data)
        if serializer.is_valid():
            is_post_like = request.data.get('post')
            if is_post_like:
                is_already_exists = Like.objects.filter(post=request.data['post'],
                                                        user=request.data['user']).first()
                if is_already_exists:
                    return Response(status=tbw_status.STATUS_220_ALREADY_LIKED)
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            is_already_exists = Like.objects.filter(comment=request.data['comment'],
                                                    user=request.data['user']).first()
            if is_already_exists:
                return Response(status=tbw_status.STATUS_220_ALREADY_LIKED)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


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
