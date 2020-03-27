from django.contrib import admin
from django.urls import path

from api.views import TopicView, MiniChatMessagesView, PostsView, CommentsView, \
    UserProfileView, UsersView, GetUserView, RegistrationView, GetTopicView, LikesView, TopicViewSet

viewset_urlpatterns = [
    path('topics/', TopicViewSet.as_view({'post': "create"}), name='create-topic'),
    path('topics/<int:topic_id>', TopicViewSet.as_view({'patch': "update"}), name='update-topic'),
    path('topics/<int:topic_id>/', TopicViewSet.as_view({'get': "retrieve"}), name='get-topic'),
    path('topics/<int:topic_id>/', TopicViewSet.as_view({'delete': "destroy"}), name='delete-topic'),
    path('topics/<str:section>/', TopicViewSet.as_view({'get': "topics_by_section"}), name='topics-section'),
    path('topics/<str:section>/search/', TopicViewSet.as_view({'get': "search"}), name='topic-section-search'),
]

urlpatterns = [
                  # REST API
                  # path('topics/', TopicView.as_view(), name='topics'),
                  # path('topics/<int:topic_id>/', GetTopicView.as_view(), name='get-topic'),
                  path('minichat-messages/', MiniChatMessagesView.as_view(), name='minichat-messages'),
                  path('posts/', PostsView.as_view(), name='posts'),
                  path('comments/', CommentsView.as_view(), name='comments'),
                  path('user/<int:id>', UserProfileView.as_view(), name='profile'),
                  path('get-user/', GetUserView.as_view(), name='get-user'),
                  path('users/', UsersView.as_view(), name='users'),
                  path('likes/', LikesView.as_view(), name='likes'),

                  # Registration
                  path('register/', RegistrationView.as_view(), name='registration')
              ] + viewset_urlpatterns
