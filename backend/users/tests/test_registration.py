from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.tests.factories import UserFactory


class TestUser(APITestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_user_registration(self):
        """
        Tests registration flow
        """
        pass
