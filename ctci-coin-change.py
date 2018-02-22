import time

a_time = time.time()
target, num_coins = map(int,input().split())
coins = list(map(int,input().split()))
b_time = time.time()
print("input:", target, num_coins, "\ncoins:", coins)
print(round(b_time - a_time, 3), "secs")

mem = [[None for i in range(50)] for i in range(251)]
def change_combs(target, coin_idx):
    if coin_idx >= num_coins:
        return 1 if target == 0 else 0
    elif mem[target][coin_idx] is None:
        c0 = coins[coin_idx]
        mem[target][coin_idx] = change_combs(target, coin_idx + 1) + (0 if c0 > target else change_combs(target - c0, coin_idx))
    return mem[target][coin_idx]

a_time = time.time()
c = change_combs(target, 0)
b_time = time.time()
print("\nresult:", c)
print(round(b_time - a_time, 3), "secs")
