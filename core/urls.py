from django.contrib import admin
from django.urls import path

from core.views import TopicView, MiniChatMessagesView, PostsView, CommentsView, UserProfileView, UsersView, \
    GetUserView, RegistrationView, HomeView

urlpatterns = [
    # REST API
    path('topics/', TopicView.as_view()),
    path('minichat-messages/', MiniChatMessagesView.as_view()),
    path('posts/', PostsView.as_view()),
    path('comments/', CommentsView.as_view()),
    path('user/<int:id>', UserProfileView.as_view()),
    path('get-user/', GetUserView.as_view()),
    path('users/', UsersView.as_view()),

    # Registration
    path('register/', RegistrationView.as_view())
]