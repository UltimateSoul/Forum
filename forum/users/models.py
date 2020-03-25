from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone


def user_directory_path(self, filename):
    return f'avatars/user_{self.id}/{filename}'


def team_directory_path(self, filename):
    return f'avatars/team_{self.id}/{filename}'


class User(AbstractUser):
    GENDER_CHOICES = [('MALE', "Male"),
                      ('FEMALE', 'Female'),
                      ('OTHER', 'Other')]
    avatar = models.ImageField(blank=True, null=True,
                               upload_to=user_directory_path)
    popularity = models.PositiveIntegerField(default=0)
    blood_coins = models.PositiveIntegerField(default=0)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10,
                              default="Male")
    game_nickname = models.CharField(blank=True, null=True, max_length=50)
    birth_date = models.DateField(blank=True, null=True)
    violations = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __repr___(self):
        return f'User({self.username})'

    def get_age(self):
        return timezone.now() - self.birth_date

    def prepare_to_save(self):
        if self.avatar:
            self.avatar.delete()
        return


class Team(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='team',
                              null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    avatar = models.ImageField(blank=True, null=True, upload_to=team_directory_path)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='team_member')

    def __str__(self):
        return self.name

