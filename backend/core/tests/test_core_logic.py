from datetime import datetime, timedelta

from rest_framework.test import APITestCase

from api.models import Topic
from api.tests.factories import TopicFactory
from core.models import UserNotification
from core.tasks import delete_moderators_removed_topics
from shop import constants
from shop.helpers import calculate_coins_for_user
from users.tests.factories import UserFactory


class TestCoreLogic(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_coins_purchase_functionality(self):
        """Checks that coins calculates properly"""

        calculate_coins_for_user(user=self.user, amount=constants.CENTS_FOR_500_COINS)
        self.assertEqual(self.user.coins, constants.COINS_500)
        self.user.coins = 0
        self.user.save()
        notification_message = UserNotification.get_notification_text(
            UserNotification.SUCCESSFUL_COINS_PURCHASE,
            username=self.user.username,
            amount=constants.COINS_500
        )
        notification = UserNotification.objects.last()
        self.assertEqual(notification.message, notification_message)
        calculate_coins_for_user(user=self.user, amount=constants.CENTS_FOR_750_COINS)
        self.assertEqual(self.user.coins, constants.COINS_750)
        self.user.coins = 0
        self.user.save()
        calculate_coins_for_user(user=self.user, amount=constants.CENTS_FOR_1000_COINS)
        self.assertEqual(self.user.coins, constants.COINS_1000)
        self.user.coins = 0
        self.user.save()
        calculate_coins_for_user(user=self.user, amount=constants.CENTS_FOR_2000_COINS)
        self.assertEqual(self.user.coins, constants.COINS_2000)
        self.user.coins = 0
        self.user.save()
        calculate_coins_for_user(user=self.user, amount=constants.CENTS_FOR_5000_COINS)
        self.assertEqual(self.user.coins, constants.COINS_5000)
        self.user.coins = 0
        self.user.save()
        calculate_coins_for_user(user=self.user, amount=constants.CENTS_FOR_10000_COINS)
        self.assertEqual(self.user.coins, constants.COINS_10000)
        self.user.coins = 0
        self.user.save()

    def test_delete_moderators_removed_topics(self):
        two_weeks_ago = datetime.now() - timedelta(days=14)
        for index in range(5):
            TopicFactory(removed_by_moderator=True,
                         removed_at=two_weeks_ago)
        delete_moderators_removed_topics()
        existing_topics = Topic.objects.all()
        self.assertFalse(bool(existing_topics))