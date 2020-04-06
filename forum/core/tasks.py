from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from celery.task import periodic_task
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from Forum import celery_app
from users.helpers import constants
from users.models import UserTeamRequest

User = get_user_model()


@celery_app.task
def send_team_request_state_email(team_request_id):
    team_request = UserTeamRequest.objects.get(id=team_request_id)
    team = team_request.team
    user = User.objects.get(id=team_request.user_id)
    if team_request.approved:
        email_subject = 'Your team request was successfully approved!'
        message = render_to_string('core/accepted_team_request.html', {
            'user': user,
            'team': team
        })
    else:
        email_subject = 'I`m a'
        message = render('core/accepted_team_request.html', {
            'user': user,
            'team': team
        })
    email = EmailMessage(
        email_subject, message, from_email=settings.FROM_EMAIL, to=[user.email]
    )
    email.content_subtype = 'html'
    email.send()


@periodic_task(run_every=timedelta(days=constants.COINS_PERIOD))
def calculate_coins():
    """Calculates coins for all ACTIVE users"""

    active_users = User.get_active_users()
    for active_user in active_users:
        active_user.calculate_blood_coins()


@celery_app.task
def send_confirmation_email(user_pk, domain, token, user_email):
    email_subject = 'Activate your forum account.'
    message = render_to_string('users/email_confirmation.html', {
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user_pk)),
        'token': token,
    })
    email = EmailMessage(
        email_subject, message, from_email=settings.FROM_EMAIL, to=[user_email]
    )
    email.content_subtype = 'html'
    email.send()
