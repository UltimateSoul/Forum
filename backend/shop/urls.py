from django.urls import path

from shop.views import PaymentView, PaymentIntent
from shop.webhooks import StripeWebhooks

urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
    path('create-payment-intent/', PaymentIntent.as_view(), name='create-payment-intent'),
    path('stripe-webhooks/', StripeWebhooks.as_view(), name='stripe-webhooks'),
]
