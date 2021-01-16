import re

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api import services
from api.tests.factories import TopicFactory, PostFactory
from users.tests.factories import UserFactory


class TestViews(APITestCase):

    def setUp(self) -> None:
        pass

    def test_get_most_popular_topics(self):
        """Tests that sorting of the most popular topics works fine"""
        author = UserFactory()
        for index in range(1, 10):
            topic = TopicFactory(
                author=author,
                body=f'topic {index}',
            )
            services.add_like(topic, author)
            for comment_index in range(index):
                PostFactory(
                    author=author,
                    topic=topic,
                    body=f'comment {comment_index}'
                )

        response = self.client.get(reverse('core:get-popular-topics'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        for topic in response.data:
            self.assertTrue(int(re.findall(r'[\d]+', topic.get('body'))[0]) > 4)
