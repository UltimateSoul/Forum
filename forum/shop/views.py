from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import stripe

from shop.helpers import get_money_for_coins
from shop.serializers import CoinsSerializer

stripe.api_key = settings.STRIPE_SECRET_API_KEY


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):  # noqa
        return Response


class PaymentIntent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):  # noqa
        serializer = CoinsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        money = get_money_for_coins(serializer.data.get('amount'))
        if not money:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        intent = stripe.PaymentIntent.create(amount=money,
                                             currency='usd',
                                             metadata={'integration_check': 'accept_a_payment'},)
        return Response({'secret': intent.client_secret}, status=status.HTTP_201_CREATED)
