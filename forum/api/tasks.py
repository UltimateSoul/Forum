from datetime import timedelta

from django.contrib.auth import get_user_model
from celery.task import periodic_task

User = get_user_model()


@periodic_task(run_every=timedelta(days=7))
def calculate_bloodcoins():
    """Calculates bloodcoins for all ACTIVE users"""

    active_users = User.get_active_users()