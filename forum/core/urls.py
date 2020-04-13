from django.urls import path

from core.search.urls import urlpatterns as search_urls
from core.views import MostPopularTopicsView


urlpatterns = [
    path('get-popular-topics/', MostPopularTopicsView.as_view(), name='get-popular-topics')
] + search_urls
