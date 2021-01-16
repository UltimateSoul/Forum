import datetime

import factory
from django.contrib.auth import get_user_model

from users.models import Team, Rank, TeamMember, UserTeamRequest

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = "Test_Username"
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


class TeamFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Team

    name = 'SoulHunters'
    description = 'Are you strong enough to hunt souls?'


class RankFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Rank

    name = 'Test Rank'


class TeamMemberFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = TeamMember


class UserTeamRequestFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = UserTeamRequest






