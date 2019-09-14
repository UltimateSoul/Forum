from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils import timezone


def user_directory_path(self, filename):
    return f'avatars/user_{self.id}/{filename}'


def team_directory_path(self, filename):
    return f'avatars/team_{self.id}/{filename}'


class User(AbstractUser):
    GENDER_CHOICES = [('MALE', "Male"),
                      ('FEMALE', 'Female'),
                      ('OTHER', 'Other')]
    avatar = models.ImageField(blank=True, null=True, upload_to=user_directory_path)
    popularity = models.PositiveIntegerField(default=0)
    blood_coins = models.PositiveIntegerField(default=0)
    city = models.CharField(blank=True, null=True, max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, default="Male")
    game_nickname = models.CharField(blank=True, null=True, max_length=50)
    birth_date = models.DateTimeField(blank=True, null=True)
    violations = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str___(self):
        return self.first_name + self.last_name

    def get_age(self):
        return timezone.now() - self.birth_date


class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    avatar = models.ImageField(blank=True, null=True, upload_to=team_directory_path)
    member = models.ForeignKey(User, null=True, blank=True, related_name='team', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

