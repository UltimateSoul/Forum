from django.urls import path

from core.search.urls import urlpatterns as search_urls
from core.views import MostPopularTopicsView, UserNotificationListView, UserNotificationDestroyView


urlpatterns = [
    path('get-popular-topics/', MostPopularTopicsView.as_view(), name='get-popular-topics'),
    path('notifications-list/', UserNotificationListView.as_view(), name='get-user-notifications'),
    path('delete-notification/<int:pk>/', UserNotificationDestroyView.as_view(), name='delete-user-notification'),
] + search_urls
