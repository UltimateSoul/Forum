from django.contrib.contenttypes.models import ContentType
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from api.models import Topic, Like, Comment, Post
from api.tests.factories import TopicFactory, PostFactory, CommentFactory
from users.models import UserTeamRequest, Team
from users.tests.factories import UserFactory, AnotherUserFactory, TeamFactory, RankFactory, TeamMemberFactory, \
    UserTeamRequestFactory
from django.urls import reverse
from api.helpers import status as forum_status


class TestProfileView(APITestCase):

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
        self.assertTrue(user_data.get('coins') == self.user.coins)

    def test_user_profile_view_constraint(self):
        """Checks flow when user goes to another user profile"""
        another_user = AnotherUserFactory()
        params = {'id': another_user.id}
        profile_response = self.client.get(reverse('api:profile', kwargs=params))
        self.assertTrue(profile_response.status_code == 200)
        user_data = profile_response.data
        self.assertFalse(bool(user_data.get('coins')))
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


class TestTopicViewSet(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        token = Token.objects.get(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_topic_viewset_list(self):
        """Testing TopicViewSet list of topics by section functionality"""
        TopicFactory()
        TopicFactory(title='Test Title2',
                     body='Test body',
                     description='Test description',
                     section=Topic.CONVERSATION)
        TopicFactory(title='Test Title3',
                     body='Test body',
                     description='Test description',
                     section=Topic.CONVERSATION)
        data = {'section': Topic.CONVERSATION}
        response = self.client.get(reverse('api:topics-by-section'), data=data)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        data = {'section': Topic.IDEAS}
        response = self.client.get(reverse('api:topics-by-section'), data)
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
        response = self.client.post(reverse('api:topics-list'), data)
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
        response = self.client.patch(reverse('api:topics-detail', kwargs={'topic_id': topic.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        topic = Topic.objects.get(id=topic.id)
        self.assertEqual(topic.description, data['description'])
        self.assertEqual(topic.body, data['body'])

    def test_retrieve_topic_viewset(self):
        """Testing TopicViewSet retrieve functionality"""

        topic = TopicFactory(author=self.user)
        response = self.client.get(reverse('api:topics-detail', kwargs={'topic_id': topic.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), topic.title)

    def test_delete_topic_viewset(self):
        """Tests TopicViewSet destroy functionality"""

        topic = TopicFactory(author=self.user)
        response = self.client.delete(reverse('api:topics-detail', kwargs={'topic_id': topic.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        superuser = UserFactory(is_superuser=True, is_staff=True, username='superuser')
        token = Token.objects.get(user=superuser)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')
        response = self.client.delete(reverse('api:topics-detail', kwargs={'topic_id': topic.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Topic.objects.filter(id=topic.id).last())

    def test_like_topic_viewset(self):
        """Tests TopicViewSet like functionality"""

        topic = TopicFactory(author=self.user)
        response = self.client.post(reverse('api:topics-like', kwargs={'topic_id': topic.id}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        obj_type = ContentType.objects.get_for_model(topic)
        likes = Like.objects.filter(
            content_type=obj_type, object_id=topic.id, user=self.user)
        self.assertTrue(likes.exists())

    def test_unlike_topic_viewset(self):
        """Tests TopicViewSet unlike functionality"""

        topic = TopicFactory(author=self.user)
        self.client.post(reverse('api:topics-like', kwargs={'topic_id': topic.id}))
        response = self.client.post(reverse('api:topics-unlike', kwargs={'topic_id': topic.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj_type = ContentType.objects.get_for_model(topic)
        likes = Like.objects.filter(
            content_type=obj_type, object_id=topic.id, user=self.user)
        self.assertFalse(likes.exists())

    def test_is_liked_topic_viewset(self):
        """Tests TopicViewSet fans functionality"""

        topic = TopicFactory(author=self.user)
        self.client.post(reverse('api:topics-like', kwargs={'topic_id': topic.id}))
        response = self.client.get(reverse('api:topics-fans', kwargs={'topic_id': topic.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data[0]
        self.assertEqual(data.get('username'), self.user.username)
        self.assertEqual(data.get('game_nickname'), self.user.game_nickname)


class TestPostsViewSet(APITestCase):
    """Tests all PostsViewSet functionality"""

    def setUp(self) -> None:
        self.user = UserFactory()
        token = Token.objects.get(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')
        self.topic = TopicFactory(author=self.user)
        self.post1 = PostFactory(author=self.user, topic=self.topic)
        self.post2 = PostFactory(author=self.user, topic=self.topic, body='Test post 2')

    def test_get_posts_by_topic(self):
        """Get all posts of particular topic"""
        data = {'topic': self.topic.id}
        response = self.client.get(reverse('api:posts-list'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)

    def test_patch_post_by_user(self):
        """Tests that user can edit post"""

        data = {
            'body': 'Edited post body'
        }
        response = self.client.patch(reverse('api:posts-detail', kwargs={'pk': self.post1.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['body'], response.data.get('body'))

    def test_delete_post_by_user(self):
        """Users cannot delete their """

        response = self.client.delete(reverse('api:posts-detail', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_successfult_post_deletion(self):
        """Tests that moderators and admins are able to delete posts"""
        self.user.is_moderator = True
        self.user.save()
        response = self.client.delete(reverse('api:posts-detail', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)


class TestCommentsViewSet(APITestCase):
    """Tests all CommentsViewSet functionality"""

    def setUp(self) -> None:
        self.user = UserFactory()
        token = Token.objects.get(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')
        self.topic = TopicFactory(author=self.user)
        self.post = PostFactory(author=self.user, topic=self.topic)
        self.comment1 = CommentFactory(author=self.user, post=self.post)

    def test_get_comments_by_post(self):
        """Get all comments of particular post"""

        CommentFactory(author=self.user, body='Test comment 2', post=self.post)
        data = {
            'post': self.post.id,
        }
        response = self.client.get(reverse('api:comments-list'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)

    def test_delete_comment(self):
        """Test user try to delete comment"""
        response = self.client.delete(reverse('api:comments-detail', kwargs={'pk': self.comment1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Comment.objects.all().exists())

    def test_successful_comment_deletion(self):
        """Tests that moderators and superusers can delete comments"""

        self.user.is_moderator = True
        self.user.save()
        response = self.client.delete(reverse('api:comments-detail', kwargs={'pk': self.comment1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.all().exists())

        self.comment1 = CommentFactory(author=self.user, post=self.post)
        self.user.is_moderator = False
        self.user.is_superuser = True
        self.user.save()

        response = self.client.delete(reverse('api:comments-detail', kwargs={'pk': self.comment1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.all().exists())


class TestRanksViewSet(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()
        token = Token.objects.get(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')
        self.team = TeamFactory(owner=self.user)

    def test_get_team_ranks(self):
        """Tests get_team_ranks logic"""
        RankFactory(name='rank1', team=self.team)
        RankFactory(name='rank2', team=self.team)
        RankFactory(name='rank3', team=self.team)
        RankFactory(name='rank4', team=self.team)
        params = {'teamID': self.team.id}
        response = self.client.get(reverse('api:ranks-get-team-ranks'), params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_is_team_owner_rank_permission(self):
        """Tests IsTeamOwnerRankPermission, only team owners can edit and create ranks"""

        weak = RankFactory(name='weak soul', team=self.team)
        middle = RankFactory(name='middle soul', team=self.team)
        non_owner = AnotherUserFactory()
        params = {'pk': weak.id}
        edited_weak_name_name = 'small weak soul'
        edited_middle_name_name = 'edited middle soul'
        data = {'name': edited_weak_name_name}
        response = self.client.patch(reverse('api:ranks-detail', kwargs=params), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), edited_weak_name_name)

        token = Token.objects.get(user=non_owner)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'name': edited_middle_name_name}
        params = {'pk': middle.id}
        response = self.client.patch(reverse('api:ranks-detail', kwargs=params), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestTeamViewSet(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        token = Token.objects.get(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')
        self.team = TeamFactory(owner=self.user)

    def test_get_teams(self):
        """Tests that users can successfully fetch data about teams"""
        owner2 = AnotherUserFactory()
        owner3 = AnotherUserFactory(username='team owner 3', email='teamowner3@gmail.com')
        TeamFactory(owner=owner2, name='second team')
        TeamFactory(owner=owner3, name='third team')

        usual_user = UserFactory(
            username='usualuser',
            email='default@email.com'
        )
        token = Token.objects.get(user=usual_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.get(reverse('api:teams-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 3)

    def test_create_new_team(self):
        """Tests that users without team can create them"""
        default_user = AnotherUserFactory()
        token = Token.objects.get(user=default_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {
            'name': 'Griffons',
            'description': 'Only strong souls can be joined us.'
        }
        response = self.client.post(reverse('api:teams-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Team.objects.filter(name=data['name']).exists())

    def test_cannot_create_new_team(self):
        """Tests that users with team cannot create them"""

        data = {
            'name': 'Griffons',
            'description': 'Only strong souls can be joined us.'
        }
        response = self.client.post(reverse('api:teams-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owners_can_edit_team_data(self):
        """Tests that team owners can edit team data"""

        data = {
            'description': 'Edited description',
            'name': 'Edited Name'
        }
        response = self.client.patch(reverse('api:teams-detail', kwargs={'pk': self.team.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        team = Team.objects.get(id=self.team.id)
        self.assertEqual(team.name, data['name'])
        self.assertEqual(team.description, data['description'])

    def test_get_team_for_user(self):
        """Tests get-team-for-user action functionality"""

        response = self.client.get(reverse('api:teams-get-team-for-user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('team_id'), self.team.id)

        user_without_team = AnotherUserFactory()
        token = Token.objects.get(user=user_without_team)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.get(reverse('api:teams-get-team-for-user'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        team_member = TeamMemberFactory(
            user=UserFactory(
                username='Team Member',
                email='teammember@gmail.com',
                game_nickname='team_member',
            ),
            team=TeamFactory(
                name='Soul Eaters',
                description='We`ll destroy all the souls. And the age of darkness will come'
            ),
            rank=RankFactory(name='Weak Soul')
        )
        token = Token.objects.get(user=team_member.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = self.client.get(reverse('api:teams-get-team-for-user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('team_id'), team_member.team.id)


class TestUserTeamRequestViewSet(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        token = Token.objects.get(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')
        self.team = TeamFactory(owner=self.user)
        self.another_user1 = AnotherUserFactory()
        self.another_user2 = AnotherUserFactory(
            username='anotheruser2',
            email='anotheruser2@gmail.com'
        )
        self.user_team_request = UserTeamRequestFactory(
            user=self.another_user1,
            team=self.team,
        )
        self.user_team_request = UserTeamRequestFactory(
            user=self.another_user2,
            team=self.team,
        )

    def test_get_requests_for_team_by_owner(self):
        """Checks getting all requests for particular team by team owner"""

        params = {'teamID': self.team.id}
        response = self.client.get(reverse('api:user-team-requests-get-requests-for-team'), params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)

    def test_get_request_only_from_one_team(self):
        """Checks that team owner will get only requests from his team"""
        another_user3 = AnotherUserFactory(username='anotheruser3', email='anotheruser3@gmail.com')
        another_user4 = AnotherUserFactory(username='anotheruser4', email='anotheruser4@gmail.com')
        another_user5 = AnotherUserFactory(username='anotheruser5', email='anotheruser5@gmail.com')
        another_user6 = AnotherUserFactory(username='anotheruser6', email='anotheruser6@gmail.com')
        another_team = TeamFactory(owner=another_user3,
                                   name='Soul Eaters',
                                   description='We`ll destroy all the souls. And the age of darkness will come')
        UserTeamRequestFactory(
            user=another_user4,
            team=another_team,
        )
        UserTeamRequestFactory(
            user=another_user5,
            team=another_team,
        )
        UserTeamRequestFactory(
            user=another_user6,
            team=another_team,
        )
        params = {'teamID': self.team.id}
        response = self.client.get(reverse('api:user-team-requests-get-requests-for-team'), params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)

    def test_get_requests_for_team_by_user(self):
        """Checks that usual user can't fetch requests data"""

        token = Token.objects.get(user=self.another_user1)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')
        params = {'teamID': self.team.id}
        response = self.client.get(reverse('api:user-team-requests-get-requests-for-team'), params)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_request_for_team(self):
        """Tests that user can create requests"""

        usual_user = UserFactory(
            username='Usual User',
            email='usualuser@gmail.com',
        )
        token = Token.objects.get(user=usual_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'team': self.team.id}
        response = self.client.post(reverse('api:user-team-requests-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_created_once(self):
        """Tests that request for user created only once"""

        usual_user = UserFactory(
            username='Usual User',
            email='usualuser@gmail.com',
        )
        token = Token.objects.get(user=usual_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'team': self.team.id}
        self.client.post(reverse('api:user-team-requests-list'), data=data)  # first request
        response = self.client.post(reverse('api:user-team-requests-list'), data=data)  # second request
        self.assertEqual(response.status_code, forum_status.STATUS_222_USER_ALREADY_REQUESTED)

    def test_team_owner_approved_request(self):
        """Tests owner approve user team request flow"""
        data = {
            'approved': True,
        }
        response = self.client.patch(reverse('api:user-team-requests-detail',
                                             kwargs={'pk': self.user_team_request.id}),
                                     data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        team_request = UserTeamRequest.objects.get(id=self.user_team_request.id)
        self.assertTrue(team_request.approved)
        self.assertTrue(team_request.email_was_send)

    def test_team_owner_rejected_request(self):
        """Tests owner reject user team request flow"""
        data = {
            'approved': False,
        }
        response = self.client.patch(reverse('api:user-team-requests-detail',
                                             kwargs={'pk': self.user_team_request.id}),
                                     data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        team_request = UserTeamRequest.objects.get(id=self.user_team_request.id)
        self.assertFalse(team_request.approved)
        self.assertTrue(team_request.email_was_send)
