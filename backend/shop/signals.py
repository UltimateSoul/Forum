import stripe
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from shop.models import UserShopProfile

stripe.api_key = settings.STRIPE_SECRET_API_KEY


@receiver(pre_save, sender=UserShopProfile)
def create_customer(sender, instance=None, **kwargs):  # noqa
    if instance.user.email and not instance.customer_id:
        customer = stripe.Customer.create(
            email=instance.user.email
        )
        instance.customer_id = customer.id