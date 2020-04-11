from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import MiniChatMessagesView, PostsViewSet, CommentsViewSet, TopicViewSet, TeamViewSet, RanksViewSet,\
    TeamRequestViewSet, UsersViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'posts', PostsViewSet, basename='posts')
router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'topics', TopicViewSet, basename='topics')
router.register(r'teams', TeamViewSet, basename='teams')
router.register(r'ranks', RanksViewSet, basename='ranks')
router.register(r'user-team-requests', TeamRequestViewSet, basename='user-team-requests')

urlpatterns = [
    path('minichat-messages/', MiniChatMessagesView.as_view(), name='minichat-messages'),
    ] + router.urls