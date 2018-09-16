# https://www.hackerrank.com/challenges/ctci-coin-change

import time

TIME_A = time.time()
TARGET, NUM_COINS = map(int, input().split())
COINS = list(map(int, input().split()))
TIME_B = time.time()
print("input:", TARGET, NUM_COINS, "\ncoins:", COINS)
print(round(TIME_B - TIME_A, 3), "secs")

MEM = [[None for i in range(50)] for i in range(251)]


def change_combs(target, coin_idx):
    if coin_idx >= NUM_COINS:
        return 1 if target == 0 else 0
    elif MEM[target][coin_idx] is None:
        c_0 = COINS[coin_idx]
        MEM[target][coin_idx] = change_combs(target, coin_idx + 1) + (
            0 if c_0 > target else change_combs(target - c_0, coin_idx)
        )
    return MEM[target][coin_idx]


TIME_A = time.time()
COMBS = change_combs(TARGET, 0)
TIME_B = time.time()
print("\nresult:", COMBS)
print(round(TIME_B - TIME_A, 3), "secs")
