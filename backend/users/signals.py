import stripe
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from shop.models import UserShopProfile

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_API_KEY


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):  # noqa
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_shop_profile(sender, instance=None, created=False, **kwargs):  # noqa
    if created:
        UserShopProfile.objects.create(user=instance)

