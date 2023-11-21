"""Common CS Algorithms"""
import random
from typing import Sequence


def quick_sort(s: "Sequence"):
    """
    Quick sort algorithm
    Worst case time: O(N^2)
    Average case time: O(NlogN)
    https://en.wikipedia.org/wiki/Quicksort

    Pick a approximately mid value as the pivot
    Place values less and more than pivot before and after it respectively
    Recursively sort the lower and higher list of values then merge

    :return: sequence sorted in ascending order
    """
    q = list(s)  # consume all elements of sequence
    # print([q])
    n = len(q)  # count final number of elements
    if n < 2:  # no sorting to be done
        return q
    elif n == 2:  # simple sort case
        return q[::-1] if q[0] > q[1] else q
    else:
        m = n // 2
        p = q[m]  # pivot value
        # NOTE: this could be swapped in place
        return [
            *quick_sort(n for n in q if n < p),
            *(n for n in q if n == p),
            *quick_sort(n for n in q if n > p),
        ]


def bubble_sort(s: "Sequence", gap: "int" = 1):
    """
    Bubble sort algorithm
    Worst case time: O(N^2)
    Average case time: O(NlogN)
    https://en.wikipedia.org/wiki/Comb_sort
    https://en.wikipedia.org/wiki/Shellsort

    [prefer insertion sort]
    Starting from one end of the sequence and moving to the opposite end
    Using gap pick the next two values and swap them into correct positions
    Move to the next two values and repeat until no swaps are needed

    :return: sequence sorted in ascending order
    """
    q = list(s)  # consume all elements of sequence
    # print([q])
    n = len(q)  # count final number of elements

    for g in range(gap, 0, -1):  # NOTE: alternatively reduce gap by half
        # print("gap", g)
        for l in range(n - g, g - 1, -1):
            did_swap = False
            for i in range(l):
                a = q[i]
                b = q[i + g]
                if a > b:
                    did_swap = True
                    q[i] = b
                    q[i + g] = a

            # print(did_swap, q)
            if not did_swap:
                break

    return q


def merge_sort(q):
    return q


def heap_sort(q):
    return q


def selection_sort(q):
    return q


def insertion_sort(q):
    return q


def jumble(s: "Sequence"):
    """Shuffle and return new list"""
    ss = [*s]
    random.shuffle(ss)
    return ss


SORTING_TESTCASES = [
    jumble([n + 1 for n in range(5)]),
    jumble([n + 1 for n in range(8)]),
    jumble([n + 1 for n in range(13)]),
    jumble([n + 1 for n in range(21)]),
]


def test_quick_sort():
    """Validate quick sort against python default sorting"""
    for tc in SORTING_TESTCASES:
        assert quick_sort(tc) == sorted(tc)


def test_bubble_sort():
    """Validate bubble sort against python default sorting"""
    for tc in SORTING_TESTCASES:
        assert bubble_sort(tc) == sorted(tc)


def test_comb_sort():
    """Validate comb shell sort against python default sorting"""
    for tc in SORTING_TESTCASES:
        assert bubble_sort(tc, len(tc) // 2) == sorted(tc)


# run tests
test_quick_sort()
test_bubble_sort()
test_comb_sort()
