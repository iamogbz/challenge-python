# https://www.hackerrank.com/challenges/ctci-contacts

import time

partials = {}

a_time = time.time()
n = int(input().strip())
for a0 in range(n):
    op, name = input().strip().split(" ")
    if op == "add":
        for a1 in [name[0:i] for i in range(len(name) + 1)]:
            partials[a1] = 1 if a1 not in partials else partials[a1] + 1
    elif op == "find":
        print(partials[name] if name in partials else 0)
b_time = time.time()
print("parsing:", b_time - a_time)
print("partials:", len(partials))
