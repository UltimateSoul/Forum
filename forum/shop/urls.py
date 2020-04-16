from django.urls import path

from core.search.urls import urlpatterns as search_urls
from shop.views import PaymentView, PaymentIntent

urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
    path('create-payment-intent/', PaymentIntent.as_view(), name='create-payment-intent'),
] + search_urls
