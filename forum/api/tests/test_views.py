from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from users.tests.factories import UserFactory, AnotherUserFactory
from django.urls import reverse


class TestViews(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()
        token = Token.objects.get(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_user_profile_view_success(self):
        """Checks flow when user goes to his profile"""
        params = {'id': self.user.id}
        profile_response = self.client.get(reverse('api:profile', kwargs=params))
        self.assertTrue(profile_response.status_code == 200)
        user_data = profile_response.data
        self.assertTrue(user_data.get('username') == self.user.username)
        self.assertTrue(user_data.get('game_nickname') == self.user.game_nickname)
        self.assertTrue(user_data.get('email') == self.user.email)
        self.assertTrue(user_data.get('description') == self.user.description)
        self.assertTrue(user_data.get('gender') == self.user.gender)
        self.assertTrue(user_data.get('blood_coins') == self.user.blood_coins)

    def test_user_profile_view_constraint(self):
        """Checks flow when user goes to another user profile"""
        another_user = AnotherUserFactory()
        params = {'id': another_user.id}
        profile_response = self.client.get(reverse('api:profile', kwargs=params))
        self.assertTrue(profile_response.status_code == 200)
        user_data = profile_response.data
        self.assertFalse(bool(user_data.get('blood_coins')))
        self.assertFalse(user_data.get('email') == self.user.email)
        self.assertFalse(user_data.get('username') == self.user.username)
        self.assertFalse(user_data.get('description') == self.user.description)
        self.assertFalse(user_data.get('gender') == self.user.gender)
        self.assertFalse(user_data.get('birth_date') == self.user.birth_date)

    def test_user_profile_view_user_doesnt_exists(self):
        """Checks flow when user doesn`t exists in db"""
        params = {'id': 101}
        profile_response = self.client.get(reverse('api:profile', kwargs=params))
        self.assertTrue(profile_response.status_code == 404)
        self.assertEqual(profile_response.data.get('error'), 'User matching query does not exist.')