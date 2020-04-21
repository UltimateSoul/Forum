from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from core.models import UserNotification
from core.tasks import send_team_request_state_email, send_confirmation_email
from shop.helpers import calculate_coins_for_user
from users.tests.factories import UserFactory, TeamFactory, UserTeamRequestFactory


class TestNotifications(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()
        self.team = TeamFactory()
        self.team_request = UserTeamRequestFactory(
            user=self.user,
            team=self.team,
            approved=True
        )

    def test_accepted_team_request_notification(self):
        """Checks that user notification creates successfully after accepting request"""
        send_team_request_state_email(self.team_request.id)
        notification = UserNotification.objects.last()
        self.assertEqual(notification.notification_type, UserNotification.SUCCESS)
        self.assertEqual(notification.user, self.user)
        notification_message = UserNotification.get_notification_text(
            UserNotification.ACCEPTED_TEAM_REQUEST,
            username=self.user.username,
            team_name=self.team.name,
        )
        self.assertEqual(notification.message, notification_message)

    def test_rejected_team_request_notification(self):
        """Checks that user notification creates successfully after rejecting request"""

        self.team_request.approved = False
        self.team_request.save()
        send_team_request_state_email(self.team_request.id)
        notification = UserNotification.objects.last()
        self.assertEqual(notification.notification_type, UserNotification.WARNING)
        self.assertEqual(notification.user, self.user)
        notification_message = UserNotification.get_notification_text(
            UserNotification.REJECTED_TEAM_REQUEST,
            team_name=self.team.name,
        )
        self.assertEqual(notification.message, notification_message)

    def test_registered_user_notification(self):
        """Checks that user notification creates successfully after registration"""

        user_data = {
            'username': self.user.username + '2',
            'password': 'test12345',
            'email': 'testemail2@email.com',
            'game_nickname': self.user.game_nickname,
            'gender': self.user.gender,
        }
        response = self.client.post(reverse('users:registration'), user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification = UserNotification.objects.last()
        self.assertEqual(notification.notification_type, UserNotification.SUCCESS)
        notification_message = UserNotification.get_notification_text(
            UserNotification.SUCCESSFULLY_REGISTERED,
            username=self.user.username + '2',
        )
        self.assertEqual(notification.message, notification_message)

    def test_send_confirmation_email_notification(self):
        """Checks that user notification creates successfully after registration"""

        send_confirmation_email(self.user.id,
                                'http://127.0.0.1:8000',
                                '12312123',
                                self.user.email)

        notification = UserNotification.objects.last()
        self.assertEqual(notification.notification_type, UserNotification.WARNING)
        self.assertEqual(notification.user, self.user)
        notification_message = UserNotification.get_notification_text(
            UserNotification.CONFIRM_EMAIL,
            username=self.user.username,
        )
        self.assertEqual(notification.message, notification_message)
