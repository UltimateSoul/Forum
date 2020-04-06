from datetime import timedelta
from django.contrib.auth import get_user_model
from celery.task import periodic_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from Forum import celery_app
from users.helpers import constants

User = get_user_model()


@periodic_task(run_every=timedelta(days=constants.COINS_PERIOD))
def calculate_bloodcoins():
    """Calculates bloodcoins for all ACTIVE users"""

    active_users = User.get_active_users()
    for active_user in active_users:
        active_user.calculate_blood_coins()


@celery_app.task
def send_confirmation_email(user_pk, current_site, token, user_email):
    email_subject = 'Activate your forum account.'
    message = render_to_string('users/email_confirmation.html', {
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user_pk)),
        'token': token,
    })
    email = EmailMessage(
        email_subject, message, from_email='owlsoulbear@gmail.com', to=[user_email]
    )
    email.send()
