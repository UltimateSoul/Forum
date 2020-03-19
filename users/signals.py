from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        print('INSIDE THE SIGNAL. CREATING TOKEN...')
        Token.objects.create(user=instance)


@receiver(post_delete, sender=User)
def delete_auth_token(sender, **kwargs):
    # ToDo: RESOLVE SIGNALS ISSUE
    print('INSIDE THE SIGNAL. DELETING TOKEN...')
    Token.objects.get(user=kwargs.get('instance')).delete()