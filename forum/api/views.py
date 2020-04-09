from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import MiniChatMessage, Post, Comment
from api.serializers import MiniChatMessageSerializer, PostSerializer, CommentSerializer, \
    CreateTopicSerializer, CreateMiniChatMessageSerializer, EditTopicSerializer
from django.contrib.auth import get_user_model

from core.tasks import send_team_request_state_email
from users.models import Team, Rank, UserTeamRequest
from users.permissions import IsTeamOwnerRankPermission, IsTeamOwner, IsAbleToDelete
from users.serializers import UserSerializer, RestrictedUserSerializer, UserProfileSerializer, TeamSerializer, \
    RankSerializer, UserTeamRequestSerializer, CreateUserTeamRequestSerializer
from .helpers.permissions import check_ability_to_edit, check_ability_to_delete
from .mixins import LikedMixin
from .models import Topic
from .serializers import TopicSerializer
from api.helpers import status as forum_status

User = get_user_model()


class HomeView(TemplateView):
    template_name = 'api/home.html'


class TopicViewSet(ModelViewSet, LikedMixin):
    paginator = LimitOffsetPagination()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, IsAbleToDelete]
    queryset = Topic.objects.all()
    lookup_url_kwarg = 'topic_id'

    def get_object(self):
        topic_id = self.kwargs.get('topic_id')
        queryset = Topic.objects.all()
        obj = get_object_or_404(queryset, id=topic_id)
        return obj

    def list(self, request, *args, **kwargs):  # noqa
        topics = Topic.objects.all()
        queryset = self.paginator.paginate_queryset(topics, request)
        serializer = TopicSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):  # noqa
        serializer = CreateTopicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        topic = serializer.save(author=self.request.user)
        return Response(status=status.HTTP_201_CREATED, data={'topic_id': topic.id})

    def retrieve(self, request, *args, **kwargs):  # noqa
        topic = self.get_object()
        serializer = TopicSerializer(topic, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):  # noqa
        topic = self.get_object()
        is_able_to_edit = check_ability_to_edit(user=self.request.user, obj=topic)
        if is_able_to_edit:
            serializer = EditTopicSerializer(topic, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK, data={'topic_id': topic.id})
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):  # noqa
        topic = self.get_object()
        is_able_to_delete = check_ability_to_delete(user=self.request.user)
        if is_able_to_delete:
            topic.delete()
            return Response()
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['GET'], detail=False, url_name='search', url_path='search')
    def search(self, request, *args, **kwargs):  # noqa
        search_data = request.GET
        section = search_data['section'].upper()
        search_by = search_data['searchBy']
        if search_by == 'title':
            topic_exists = Topic.objects.filter(title=search_data['value'],
                                                section=section).exists()
            return Response(data={'topic_exists': topic_exists})
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, url_name='by-section', url_path='by-section')
    def topics_by_section(self, request, *args, **kwargs):  # noqa
        section = request.GET.get('section')
        topics = Topic.objects.filter(section=section.upper())
        queryset = self.paginator.paginate_queryset(topics, request)
        serializer = TopicSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class MiniChatMessagesView(APIView):
    """Mini Chat Messages Get View"""
    permission_classes = [IsAbleToDelete]

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
        return Response({'success': False,
                         'errors': mini_chat_message.error_messages})


class PostsViewSet(ModelViewSet, LikedMixin):
    """Mini Chat Messages Get View"""

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, IsAbleToDelete]

    # Add additional permission, posts can write only users with checked email

    def get_queryset(self):
        if self.request.GET.get('topic'):
            return self.queryset.filter(topic=self.request.GET.get('topic'))
        return self.queryset

    def get_serializer_context(self, *args, **kwargs):  # noqa
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(ModelViewSet, LikedMixin):
    """Mini Chat Messages Get View"""

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAbleToDelete]

    def get_queryset(self):
        if self.request.GET.get('post'):
            return self.queryset.filter(post=self.request.GET.get('post'))
        return self.queryset

    def get_serializer_context(self, *args, **kwargs):  # noqa
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserProfileView(APIView):
    """User Profile View"""

    @staticmethod
    def get(request, *args, **kwargs):  # noqa
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

    def patch(self, request, *args, **kwargs):  # noqa
        """Here user can change his profile data"""
        user_id = kwargs.get('id')
        user = request.user
        is_main_user = user.id == user_id or user.is_staff or user.is_superuser
        if is_main_user:  # checks if it`s owner of profile
            serializer = UserProfileSerializer(user, data=request.data)
            if serializer.is_valid():
                user.prepare_to_save(data=request.data)
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': 'Cheater!'})


class GetUserView(APIView):
    """Fetch user view"""

    @staticmethod
    def get(request, *args, **kwargs):  # noqa
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UsersView(APIView):
    """All Users View"""
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, *args, **kwargs):  # noqa
        if request.GET.get('email'):  # noqa
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


class TeamViewSet(ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get_queryset(self):
        if 'name' in self.request.GET:
            return self.queryset.filter(name=self.request.GET.get('name'))
        return self.queryset

    def create(self, request, *args, **kwargs):  # noqa
        """Creation team is possible only in case if user doesn't have team"""

        if self.request.user.has_team:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user.id == instance.owner.id:
            instance.delete()

    @action(methods=['GET'], detail=False)
    def get_team_for_user(self, *args, **kwargs):  # noqa
        """Returns team for user if it has team"""
        user = self.request.user
        team = Team.objects.filter(owner=user).first()
        if not team:
            team = get_object_or_404(self.queryset, members__user=user)
        return Response(data={'team_id': team.id})


class RanksViewSet(ModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer
    permission_classes = [IsAuthenticated, IsTeamOwnerRankPermission]

    @action(methods=['GET'], detail=False)
    def get_team_ranks(self, request, *args, **kwargs):  # noqa
        team_id = request.GET.get('teamID')
        ranks = Rank.objects.filter(team__id=team_id)
        serializer = self.serializer_class(ranks, many=True)
        return Response(serializer.data)


class TeamRequestViewSet(ModelViewSet):
    queryset = UserTeamRequest.objects.filter(approved=False, email_was_send=False)
    serializer_class = UserTeamRequestSerializer
    permission_classes = [IsAuthenticated, IsTeamOwner, IsAbleToDelete]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'is_request_exist':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsTeamOwner, IsAbleToDelete]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):  # noqa
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _, is_created = serializer.save()
        response_status = 201 if is_created else forum_status.STATUS_222_USER_ALREADY_REQUESTED
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=response_status, headers=headers)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_update(self, serializer):
        team_request = serializer.save()
        if not team_request.email_was_send:
            send_team_request_state_email(team_request.id)  # ToDo: add delay on PROD, need to remove for testing

    def get_serializer(self, *args, **kwargs):  # noqa
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = CreateUserTeamRequestSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    @action(methods=['GET'], detail=False, url_path='get-requests-for-team')
    def get_requests_for_team(self, request, *args, **kwargs):  # noqa

        team_id = self.request.GET.get('teamID')
        page = self.paginate_queryset(self.queryset.filter(team_id=team_id))
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': self.request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='is-request-exist')
    def is_request_exist(self, request, *args, **kwargs):  # noqa
        data = request.GET
        get_object_or_404(queryset=self.queryset,
                          user=self.request.user,
                          email_was_send=False,
                          approved=False,
                          team_id=data.get('teamID')
                          ).exists()
        return Response()
