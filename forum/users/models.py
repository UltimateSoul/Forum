import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone

from api.models import Topic, Comment, Post, MiniChatMessage
from users.helpers import constants
from users.helpers.helpers import user_directory_path, team_directory_path


class User(AbstractUser):
    GENDER_CHOICES = [('MALE', "Male"),
                      ('FEMALE', 'Female'),
                      ('OTHER', 'Other')]
    avatar = models.ImageField(blank=True, null=True,
                               upload_to=user_directory_path)
    popularity = models.PositiveIntegerField(default=0)
    coins = models.PositiveIntegerField(default=0)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10,
                              default="Male")
    game_nickname = models.CharField(blank=True, null=True, max_length=50)
    birth_date = models.DateField(blank=True, null=True)
    violations = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    is_moderator = models.BooleanField(default=False)

    @classmethod
    def get_active_users(cls) -> list:
        """Get all users that added posts/comments/topics/minichat-messages in last week"""

        users = cls.objects.filter(is_active=True)
        active_forum_users = []
        for user in users:
            if user.is_active_forum_user():
                active_forum_users.append(user)
        return active_forum_users

    def is_active_forum_user(self):
        """Checks if user has activity during last week or not"""

        now = datetime.datetime.now()
        week_ago = now - datetime.timedelta(days=constants.COINS_PERIOD)
        activity = []
        for instance in Topic, Comment, Post, MiniChatMessage:
            activity.append(instance.objects.filter(author=self, edited_at__range=[week_ago, now]).exists())
        return any(activity)

    def calculate_coins(self):
        """Calculates coins for user"""

        now = datetime.datetime.now()
        week_ago = now - datetime.timedelta(days=constants.COINS_PERIOD)

        topics = Topic.objects.filter(author=self, created_at__range=[week_ago, now])
        topics_total_likes = 0
        for topic in topics:
            topics_total_likes += topic.total_likes()

        comments = Comment.objects.filter(author=self, created_at__range=[week_ago, now])
        comments_total_likes = 0
        for comment in comments:
            comments_total_likes += comment.total_likes()

        posts = Post.objects.filter(author=self, created_at__range=[week_ago, now])
        posts_total_likes = 0
        for post in posts:
            posts_total_likes += post.total_likes()

        minichat_messages = MiniChatMessage.objects.filter(author=self, created_at__range=[week_ago, now]).count()

        topics_score = topics.count() * constants.topic_multiplier + topics_total_likes * constants.topic_likes_multiplier
        comments_score = comments.count() * constants.comment_multiplier + comments_total_likes * constants.comment_likes_multiplier
        posts_score = posts.count() * constants.post_multiplier + posts_total_likes * constants.post_likes_multiplier
        minichat_messages_score = minichat_messages * constants.minichat_message_multiplier

        coins = topics_score + comments_score + posts_score + minichat_messages_score
        self.coins += coins
        self.save()

    def __repr___(self):
        return f'User({self.username})'

    def get_age(self):
        return timezone.now() - self.birth_date

    def prepare_to_save(self, data):
        if self.avatar and data.get('avatar'):
            self.avatar.delete()


class Team(models.Model):
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='my_team',
                                 null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    avatar = models.ImageField(blank=True, null=True, upload_to=team_directory_path)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @property
    def total_members(self):
        return self.members.count()

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    rank = models.ForeignKey('Rank', blank=True, null=True, on_delete=models.SET_NULL)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f'TeamMembership(user={self.user.username}, team={self.team.name})'

    class Meta:
        verbose_name = 'TeamMember'
        verbose_name_plural = 'TeamMembers'
        ordering = ('joined_at', )


class Rank(models.Model):
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __repr__(self):
        return f'Rank(name={self.name})'


class UserTeamRequest(models.Model):
    """
    This model represents requests from users, that wants join team
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    approved = models.BooleanField(default=False)
    email_was_send = models.BooleanField(default=False)
    reject_cause = models.CharField(default='-----', max_length=255)

    def __repr__(self):
        return f'Request from {self.user.username} into {self.team.name}'
