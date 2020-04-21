import factory

from core.models import UserNotification


class UserNotificationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = UserNotification

