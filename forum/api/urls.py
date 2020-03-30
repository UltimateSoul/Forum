from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import MiniChatMessagesView, PostsViewSet, CommentsViewSet, \
    UserProfileView, UsersView, GetUserView, RegistrationView, TopicViewSet

router = DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')
router.register(r'comments', CommentsViewSet, basename='comments')

viewset_urlpatterns = [
    path('topics/', TopicViewSet.as_view({'post': "create"}), name='create-topic'),
    path('topics/', TopicViewSet.as_view({'get': "list"}), name='topics'),
    path('topic/edit/<int:topic_id>/', TopicViewSet.as_view({'patch': "partial_update"}), name='update-topic'),
    path('topic/get/<int:topic_id>/', TopicViewSet.as_view({'get': "retrieve"}), name='get-topic'),
    path('topic/delete/<int:topic_id>/', TopicViewSet.as_view({'delete': "destroy"}), name='delete-topic'),
    path('topics/<str:section>/', TopicViewSet.as_view({'get': "topics_by_section"}), name='topics-section'),
    path('topics/<str:section>/search/', TopicViewSet.as_view({'get': "search"}), name='topic-section-search'),
] + router.urls

urlpatterns = [
    # REST API
    # path('topics/', TopicView.as_view(), name='topics'),
    # path('topics/<int:topic_id>/', GetTopicView.as_view(), name='get-topic'),
    path('minichat-messages/', MiniChatMessagesView.as_view(), name='minichat-messages'),
    # path('posts/', PostsView.as_view(), name='posts'),
    # path('comments/', CommentsView.as_view(), name='comments'),
    path('user/<int:id>', UserProfileView.as_view(), name='profile'),
    path('get-user/', GetUserView.as_view(), name='get-user'),
    path('users/', UsersView.as_view(), name='users'),

    # Registration
    path('register/', RegistrationView.as_view(), name='registration')
              ] + viewset_urlpatterns
