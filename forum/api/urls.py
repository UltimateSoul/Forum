from django.contrib import admin
from django.urls import path

from api.views import TopicView, MiniChatMessagesView, PostsView, CommentsView, \
    UserProfileView, UsersView, GetUserView, RegistrationView, GetTopicView, LikesView

urlpatterns = [
    # REST API
    path('topics/', TopicView.as_view(), name='topics'),
    path('topics/<int:topic_id>/', GetTopicView.as_view(), name='get-topic'),
    path('minichat-messages/', MiniChatMessagesView.as_view(), name='minichat-messages'),
    path('posts/', PostsView.as_view(), name='posts'),
    path('comments/', CommentsView.as_view(), name='comments'),
    path('user/<int:id>', UserProfileView.as_view(), name='profile'),
    path('get-user/', GetUserView.as_view(), name='get-user'),
    path('users/', UsersView.as_view(), name='users'),
    path('likes/', LikesView.as_view(), name='likes'),

    # Registration
    path('register/', RegistrationView.as_view(), name='registration')
]