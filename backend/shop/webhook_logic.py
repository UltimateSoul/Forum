from django.contrib.auth import get_user_model

from shop.helpers import calculate_coins_for_user
from shop.mixins import StripeWebhookMixin


User = get_user_model()


def internal_webhook_logic(data):
    webhook_data = data.get('data', {'object': {}}).get('object')
    if data.get('type') == StripeWebhookMixin.SUCCEEDED_PAYMENT_INTENT:
        amount = webhook_data.get('amount')
        customer_id = webhook_data.get('customer')
        if customer_id is not None:
            try:
                user = User.objects.get(shop_profile__customer_id=customer_id)
                calculate_coins_for_user(user=user, amount=amount)
            except User.DoesNotExist:
                pass