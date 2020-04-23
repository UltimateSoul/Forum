from rest_framework.test import APITestCase

from api.models import MiniChatMessage
from api.tests.factories import TopicFactory, TagFactory
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

    def test_topic_tags(self):
        tags = ['new hero', 'rules', 'new version', 'hero update', 'bug']
        topic = TopicFactory()
        for tag in tags:
            tag_object = TagFactory(name=tag)
            topic.tags.add(tag_object)
        topic_tags = topic.tags.all()
        self.assertEqual(topic_tags.count(), len(tags))
