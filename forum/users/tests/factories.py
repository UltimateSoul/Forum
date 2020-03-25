import datetime

import factory
from django.contrib.auth import get_user_model
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = "Test Username"
    email = "test@email.com"
    game_nickname = "Test Game Nickname"
    gender = 'MALE'
    birth_date = datetime.datetime.strptime('1995-04-26T23:00:00', '%Y-%m-%dT%H:%M:%S')
    description = 'Test Description'


class AnotherUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = "anothertestuser"
    email = "anothertestuser@email.com"
    game_nickname = "Test Another Game Nickname"
    gender = 'FEMALE'
    birth_date = datetime.datetime.strptime('1999-01-06T23:00:00', '%Y-%m-%dT%H:%M:%S')
    description = 'Another Test Description'