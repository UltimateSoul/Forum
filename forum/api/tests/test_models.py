from rest_framework.test import APITestCase

from api.models import MiniChatMessage
from users.tests.factories import UserFactory


class TestModels(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_minichat_message_deletion(self):
        """Checks that redundant messages will deleted after achieving max value"""

        for number in range(10002):
            MiniChatMessage.objects.create(
                author=self.user,
                body=f'{number}'
            )
        message_count = MiniChatMessage.objects.count()
        self.assertTrue(message_count == 5002)