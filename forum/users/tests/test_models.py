from django.test import TestCase
from django.contrib.auth import get_user_model

from users.models import Team, TeamMembership

User = get_user_model()


class TestTeams(TestCase):
    def setUp(self) -> None:
        pass

    def test_creation(self):
        """Test full team creation flow and all team boundaries"""
        pass
