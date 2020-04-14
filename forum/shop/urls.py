from django.urls import path

from core.search.urls import urlpatterns as search_urls
from shop.views import PaymentView

urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
] + search_urls
