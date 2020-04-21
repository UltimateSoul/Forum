COINS_500 = 500
COINS_750 = 750
COINS_1000 = 1000
COINS_2000 = 2000
COINS_5000 = 5000
COINS_10000 = 10000
CENTS_FOR_500_COINS = 300
CENTS_FOR_750_COINS = 400
CENTS_FOR_1000_COINS = 500
CENTS_FOR_2000_COINS = 800
CENTS_FOR_5000_COINS = 1500
CENTS_FOR_10000_COINS = 2500

COINS_CENTS_DEPENDENCY = {COINS_500: CENTS_FOR_500_COINS,
                          COINS_750: CENTS_FOR_750_COINS,
                          COINS_1000: CENTS_FOR_1000_COINS,
                          COINS_2000: CENTS_FOR_2000_COINS,
                          COINS_5000: CENTS_FOR_5000_COINS,
                          COINS_10000: CENTS_FOR_10000_COINS}

CENTS_COINS_DEPENDENCY = {value: key for key, value in COINS_CENTS_DEPENDENCY.items()}
