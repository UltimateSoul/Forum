from shop import constants


def get_product_path(self, filename):
    return f'products/{filename}'


def get_money_for_coins(coins_amount):
    """Returns the amount of dollars that corresponds to the amount of coins"""

    dependency = {constants.COINS_500: constants.CENTS_FOR_500_COINS,
                  constants.COINS_750: constants.CENTS_FOR_750_COINS,
                  constants.COINS_1000: constants.CENTS_FOR_1000_COINS,
                  constants.COINS_2000: constants.CENTS_FOR_2000_COINS,
                  constants.COINS_5000: constants.CENTS_FOR_5000_COINS,
                  constants.COINS_10000: constants.CENTS_FOR_10000_COINS}
    return dependency.get(coins_amount)


def calculate_coins_for_user(user, amount):
    """Calculates coins for user and add them to user"""

    dependency = {constants.CENTS_FOR_500_COINS: constants.COINS_500,
                  constants.CENTS_FOR_750_COINS: constants.COINS_750,
                  constants.CENTS_FOR_1000_COINS: constants.COINS_1000,
                  constants.CENTS_FOR_2000_COINS: constants.COINS_2000,
                  constants.CENTS_FOR_5000_COINS: constants.COINS_5000,
                  constants.CENTS_FOR_10000_COINS: constants.COINS_10000}

    coins_amount = dependency.get(amount)
    user.coins += coins_amount
    user.save()