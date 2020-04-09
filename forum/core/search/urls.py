from django.urls import path

from core.search.views import SearchTopics

urlpatterns = [
    path('search-topics/', SearchTopics.as_view(), name='search-topics')
]
