#!/usr/bin/env python
# https://www.nytimes.com/games/digits solver

from operator import add, sub, mul, truediv
from itertools import combinations


def div(*args):
    """True division but only allow integer results"""
    res = truediv(*args)
    if int(res) == res:
        return int(res)
    else:
        raise ArithmeticError(f"Non integer result ({res}) from div{args}")


def next_step(list_n, steps: "list[str]" = ()):
    """
    Generate all next combos keeping track of performed steps
    """
    next_steps = []
    for n_1, n_2 in combinations(list_n, 2):
        unoperated_n = list(list_n)
        unoperated_n.remove(n_1)
        unoperated_n.remove(n_2)
        for op_fn in [add, sub, mul, div]:
            try:
                # sort in descending to limit negatives and fractions
                op_args = tuple(sorted((n_1, n_2), reverse=True))
                res = op_fn(*op_args)
                step = f"{op_fn.__name__}{op_args}"
                # print(f'{step} = {res}.')
                next_steps.append(([res, *unoperated_n], [*steps, step]))
            except:
                pass

    return next_steps


def find_ops(list_n, target_n):
    """DFS find and show operations used to get target number"""
    next_q = [(list_n, [])]
    while next_q:
        next_set, prev_steps = next_q.pop(0)
        next_steps = next_step(next_set, prev_steps)
        for set_n, steps in next_steps:
            if target_n in set_n:
                set_n.remove(target_n)
                print(target_n, "from", steps, "left", set_n)
                # exit on first solution found
                return
        next_q.extend(next_steps)


raw_list_n = input("Enter comma separated whole numbers: ")
int_list_n = [int(n) for n in raw_list_n.split(",")]
target_int = int(input("Enter target integer number: "))
find_ops(int_list_n, target_int)
