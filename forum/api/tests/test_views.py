from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from api.models import Topic
from api.tests.factories import TopicFactory
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

    def test_user_profile_view_user_doesnt_exist(self):
        """Checks flow when user doesn`t exists in db"""
        params = {'id': 101}
        profile_response = self.client.get(reverse('api:profile', kwargs=params))
        self.assertTrue(profile_response.status_code == 404)
        self.assertEqual(profile_response.data.get('error'), 'User matching query does not exist.')

    def test_topic_viewset_list(self):
        """Testing TopicViewSet list of topics by section functionality"""
        data = {'section': Topic.CONVERSATION}
        TopicFactory()
        TopicFactory(title='Test Title2',
                     body='Test body',
                     description='Test description',
                     section=Topic.CONVERSATION)
        TopicFactory(title='Test Title3',
                     body='Test body',
                     description='Test description',
                     section=Topic.CONVERSATION)
        response = self.client.get(reverse('api:topics-section', kwargs=data))
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        data = {'section': Topic.IDEAS}
        response = self.client.get(reverse('api:topics-section', kwargs=data), data)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_topic_viewset(self):
        """Testing TopicViewSet create topic functionality"""

        data = {
            'title': 'Test Topic',
            'description': 'Test topic description',
            'body': 'Test topic body',
            'section': 'CONVERSATION'
        }
        response = self.client.post(reverse('api:create-topic'), data)
        self.assertTrue(response.status_code == status.HTTP_201_CREATED)
        created_topic = Topic.objects.last()
        self.assertTrue(created_topic)
        self.assertEqual(created_topic.title, data['title'])
        self.assertEqual(created_topic.description, data['description'])
        self.assertEqual(created_topic.body, data['body'])
        self.assertEqual(created_topic.section, data['section'])

    def test_update_topic_viewset(self):
        """Testing TopicViewSet patch method functionality"""

        topic = TopicFactory(author=self.user)
        data = {
            'description': 'Edited Description',
            'body': 'Edited body',
            'section': topic.section
        }
        response = self.client.patch(reverse('api:update-topic', kwargs={'topic_id': topic.id}), data)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        topic = Topic.objects.get(id=topic.id)
        self.assertEqual(topic.description, data['description'])
        self.assertEqual(topic.body, data['body'])

    def test_retrieve_topic_viewset(self):
        """Testing TopicViewSet retrieve functionality"""

        topic = TopicFactory(author=self.user)
        response = self.client.get(reverse('api:get-topic', kwargs={'topic_id': topic.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), topic.title)

    def test_delete_topic_viewset(self):
        """Tests TopicViewSet destroy functionality"""

        topic = TopicFactory(author=self.user)
        response = self.client.delete(reverse('api:delete-topic', kwargs={'topic_id': topic.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        superuser = UserFactory(is_superuser=True, is_staff=True, username='superuser')
        token = Token.objects.get(user=superuser)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')
        response = self.client.delete(reverse('api:delete-topic', kwargs={'topic_id': topic.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Topic.objects.filter(id=topic.id).last())
