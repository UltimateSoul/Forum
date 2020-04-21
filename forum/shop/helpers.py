from core.models import UserNotification
from shop import constants


def get_product_path(self, filename):
    return f'products/{filename}'


def get_money_for_coins(coins_amount):
    """Returns the amount of dollars that corresponds to the amount of coins"""
    return constants.COINS_CENTS_DEPENDENCY.get(coins_amount)


def calculate_coins_for_user(user, amount):
    """Calculates coins for user and add them to user"""

    coins_amount = constants.CENTS_COINS_DEPENDENCY.get(amount)
    user.coins += coins_amount
    user.save()
    notification_message = UserNotification.get_notification_text(
        UserNotification.SUCCESSFUL_COINS_PURCHASE,
        username=user.username,
        amount=coins_amount
    )
    UserNotification.objects.create(
        user=user,
        message=notification_message,
        notification_type=UserNotification.SUCCESS
    )