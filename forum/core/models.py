from django.conf import settings
from django.db import models
from core.mixins import NotificationTextMixin


class UserNotification(models.Model, NotificationTextMixin):
    """Model that represents notifications which user can receive"""

    purpose = models.PositiveSmallIntegerField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255, null=True, blank=True)
    notification_type = models.PositiveSmallIntegerField(null=True, blank=True,
                                                         choices=NotificationTextMixin.NOTIFICATION_CHOICES)