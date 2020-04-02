from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import MiniChatMessagesView, PostsViewSet, CommentsViewSet, \
    UserProfileView, UsersView, GetUserView, TopicViewSet, TeamViewSet

router = DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')
router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'topics', TopicViewSet, basename='topics')
router.register(r'teams', TeamViewSet, basename='teams')

urlpatterns = [
    path('minichat-messages/', MiniChatMessagesView.as_view(), name='minichat-messages'),
    path('user/<int:id>', UserProfileView.as_view(), name='profile'),
    path('get-user/', GetUserView.as_view(), name='get-user'),
    path('users/', UsersView.as_view(), name='users'),
    ] + router.urls