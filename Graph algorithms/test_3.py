from graph import best_trades
import random


def test_best_trades():
    s = 0
    res = []
    # lists for keeping track of all given arguments, for debugging purposes
    all_prices = []
    all_townspeople = []
    all_maxtrades = []
    all_startingliquids = []

    # generate 10 test cases
    for _ in range(10):
        prices = []

        # add 20 liquids
        for null in range(20):
            random.seed(s)
            s += 1
            prices.append(round(random.random()*20))


        random.seed(s)
        s += 1
        # pick a relatively small max_trades
        max_trades = random.randint(0, 10)
        random.seed(s)
        s += 1
        # pick a random starting liquid
        starting_liquid = random.randint(0, 19)

        townspeople = [[]]

        # add a trade for each liquid
        for i in range(len(prices)):
            random.seed(s)
            s += 1
            townspeople[0].append((random.randint(0, 19), i, random.random()*4))

        # add 10 other trades
        for _ in range(10):
            random.seed(s)
            s += 1
            liq1 = random.randint(0, 19)
            random.seed(s)
            s += 1
            liq2 = random.randint(0, 19)
            r = random.random()*10
            townspeople.append([(liq1, liq2, r)])

        # store all arguments
        all_maxtrades.append(max_trades)
        all_startingliquids.append(starting_liquid)
        all_prices.append(prices)
        all_townspeople.append(townspeople)
        res.append(best_trades(prices, starting_liquid, max_trades, townspeople))

    return res


if __name__ == '__main__':
    print(test_best_trades())
