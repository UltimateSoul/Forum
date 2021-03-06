from datetime import timedelta, datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from celery.task import periodic_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from Forum import celery_app
from api.models import Topic
from core.models import UserNotification
from users.helpers import constants
from users.models import UserTeamRequest, TeamMember

User = get_user_model()


@celery_app.task
def send_team_request_state_email(team_request_id):
    team_request = UserTeamRequest.objects.get(id=team_request_id)
    team = team_request.team
    user = User.objects.get(id=team_request.user_id)
    if team_request.approved:
        TeamMember.objects.get_or_create(
            user=user,
            team=team
        )
        email_subject = 'Your team request was successfully approved!'
        message = render_to_string('core/accepted_team_request.html', {
            'user': user,
            'team': team
        })
        notification_message = UserNotification.get_notification_text(
            UserNotification.ACCEPTED_TEAM_REQUEST,
            username=user.username,
            team_name=team.name,
        )
        UserNotification.objects.create(
            user=user,
            purpose=UserNotification.APPROVED_TEAM_REQUEST_PURPOSE,
            message=notification_message,
            notification_type=UserNotification.SUCCESS
        )
    else:
        email_subject = 'Your team request was rejected.'
        message = render_to_string('core/rejected_team_request.html', {
            'user': user,
            'team': team
        })
        notification_message = UserNotification.get_notification_text(
            UserNotification.REJECTED_TEAM_REQUEST,
            team_name=team.name,
        )
        UserNotification.objects.create(
            user=user,
            purpose=UserNotification.REJECTED_TEAM_REQUEST_PURPOSE,
            message=notification_message,
            notification_type=UserNotification.WARNING
        )
    email = EmailMessage(
        email_subject, message, from_email=settings.FROM_EMAIL, to=[user.email]
    )
    email.content_subtype = 'html'
    email.send()
    team_request.email_was_send = True
    team_request.save()


@periodic_task(run_every=timedelta(days=constants.COINS_PERIOD))
def calculate_coins():
    """Calculates coins for all ACTIVE users"""

    active_users = User.get_active_users()
    for active_user in active_users:
        active_user.calculate_coins()


@periodic_task(run_every=timedelta(days=constants.DELETION_PERIOD))
def delete_moderators_removed_topics():
    """Finally delete topics that were removed by moderators"""

    week_ago = datetime.now() - timedelta(days=7)
    Topic.objects.filter(
        removed_by_moderator=True,
        removed_at__lte=week_ago
    ).delete()


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
    user = User.objects.get(pk=user_pk)
    notification_message = UserNotification.get_notification_text(UserNotification.CONFIRM_EMAIL,
                                                                  username=user.username)
    UserNotification.objects.create(
        user=user,
        notification_type=UserNotification.WARNING,
        message=notification_message,
        purpose=UserNotification.CONFIRM_EMAIL_PURPOSE
    )
