from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.webhook_logic import internal_webhook_logic


class StripeWebhooks(APIView):
    """Caches webhooks from stripe"""
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response()

    def post(self, request, *args, **kwargs):
        internal_webhook_logic(request.data)
        return Response()
