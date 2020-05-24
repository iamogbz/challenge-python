# https://www.hackerrank.com/challenges/circular-palindromes
# https://leetcode.com/problems/longest-palindromic-substring/solution/

import time
from collections import defaultdict
from typing import List


def all_palindromes(word: str, size: int, limit: int):
    """
    Gets the position and max size of all palidromic substrings based on
    https://en.wikipedia.org/wiki/Longest_palindromic_substring#Manacher's_algorithm
    """
    bounded_word = "@" + word + "#"
    radii = [[0] * (size + 1) for _ in range(2)]
    palindromes = defaultdict(set)
    for s in range(2):
        longest = 0
        i = 1
        while i <= size:
            while (
                bounded_word[i - 1 - longest] == bounded_word[i + longest + s]
                and longest * 2 + s < limit
            ):
                longest += 1
                if longest * 2 + s > 1:
                    palindromes[longest * 2 + s].add(i - 1 - longest)
            radii[s][i] = longest
            k = 1
            while radii[s][i - k] != (longest - k) and k < longest:
                radii[s][i + k] = min(radii[s][i - k], longest - k)
                if radii[s][i + k] * 2 + s > 1:
                    palindromes[radii[s][i + k] * 2 + s].add(
                        (i + k) - 1 - radii[s][i + k]
                    )
                k += 1
            longest = max(longest - k, 0)
            i += k

    return palindromes


def circular_palindromes(word: str, size: int):
    palindromes = all_palindromes(word + word[:-1], size * 2 - 1, size)
    # lengths = sorted(palindromes.keys(), reverse=True)
    skip = set()
    yield from []
    return
    for rotation in range(size):
        longest = 1
        for length in range(size, 1, -1):
            for start in palindromes[length]:
                if (length, start) in skip:
                    continue
                if start <= rotation:
                    skip.add((length, start))
                if start >= rotation and start + length <= rotation + size:
                    longest = length
                    break
            if longest > 1:
                break
        yield longest


# =============================================================================
# MAIN
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    N = int(input())
    S = input()
    for cycle_longest in circular_palindromes(S, N):
        print(cycle_longest)


# =============================================================================
# TESTS
# -----------------------------------------------------------------------------
import pytest


@pytest.mark.parametrize("test_case", [15, 25])
@pytest.mark.timeout(10)
def test_circular_palindromes(test_case):
    with open(f"circular-palindromes_input{test_case}.txt", "r") as f:
        size = int(f.readline())
        word = f.readline()
    time_a = time.perf_counter()
    with open(f"circular-palindromes_output{test_case}.txt", "r") as f:
        for n in circular_palindromes(word, size):
            assert str(n) == f.readline().strip()
    time_b = time.perf_counter()
    print("time: {} secs".format(round(time_b - time_a, 3)))
