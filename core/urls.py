from django.contrib import admin
from django.urls import path

from core.views import TopicView

urlpatterns = [
    path('topics/', TopicView.as_view())
]
