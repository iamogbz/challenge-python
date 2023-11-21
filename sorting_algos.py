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

    NOTE: look into insertion sort preference
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


def insertion_sort(s: "Sequence"):
    """
    Insertion sort algorithm
    Worst case time: O(N^2)
    Average case time: O(N^2)
    https://en.wikipedia.org/wiki/Insertion_sort

    Starting from one end of the sequence and moving to the opposite end
    Find the correct value position in the sorted section
    Insert the current value in the correct position shrinking the unsorted section
    Move to the next value from the unsorted section

    :return: sequence sorted in ascending order
    """
    q = list(s)  # consume all elements of sequence
    # print([q])
    n = len(q)  # count final number of elements

    for i in range(1, n):
        for p in range(i - 1, -1, -1):
            v = q[i]
            u = q[p]
            if v >= u:
                q.insert(p + 1, q.pop(i))
                break
            elif p == 0:
                q.insert(p, q.pop(i))

        # print(q)

    return q


def jumble(s: "Sequence"):
    """Shuffle and return new list"""
    ss = [*s]
    random.shuffle(ss)
    return ss


def fibs(a: "int" = 0, b: "int" = 1, n: "int" = 10):
    """Get fibonacci sub sequence"""
    if n < 1:
        return []
    return [a, *fibs(b, a + b, n - 1)]


TESTCASE_COUNT = 4
SORTING_TESTCASES = [
    ((t := [n + 1 for n in range(f)]), jumble(t)) for f in fibs(5, 8, TESTCASE_COUNT)
]


def test_quick_sort():
    """Validate quick sort"""
    for ec, tc in SORTING_TESTCASES:
        assert ec == quick_sort(tc)


def test_bubble_sort():
    """Validate bubble sort"""
    for ec, tc in SORTING_TESTCASES:
        assert ec == bubble_sort(tc)


def test_comb_sort():
    """Validate comb shell sort"""
    for ec, tc in SORTING_TESTCASES:
        assert ec == bubble_sort(tc, len(tc) // 2)


def test_insertion_sort():
    """Validate insertion sort"""
    for ec, tc in SORTING_TESTCASES:
        assert ec == insertion_sort(tc)


# run tests
test_quick_sort()
test_bubble_sort()
test_comb_sort()
test_insertion_sort()
