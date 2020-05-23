# https://www.hackerrank.com/challenges/circular-palindromes
# https://leetcode.com/problems/longest-palindromic-substring/solution/

import time
from typing import List


def all_palindromes(word: str, size: int) -> List[List[int]]:
    """
    Gets the position and max size of all palidromic substrings
    https://en.wikipedia.org/wiki/Longest_palindromic_substring#Manacher's_algorithm

    Arguments:
        word -- the word to analyse
        size -- the length of the word

    Returns:
        list of list of integers -- where each index is the center position
        of the palidrome, and each integer is the length from the center to
        the left and right to make the palidrome. A value of zero means a no
        palidrome of maximum length greater than 1 was found. With the second
        being the odd length palindromes to be offset by 1 on the input word
        i.e. word[i - 1 - maximum : i - 1 + maximum + s]
    
    Example:
        Arguments: ("aabadd", 6)
        Returns: [
            [0, 0, 1, 0, 0, 0, 1], // evens
            [0, 0, 0, 1, 0, 0, 0], // odds
        ]
    """
    bounded_word = "@" + word + "#"
    radii: List[List[int]] = [[0] * (size + 1) for _ in range(2)]
    for s in range(2):
        maximum = 0
        i = 1
        while i <= size:
            while bounded_word[i - 1 - maximum] == bounded_word[i + maximum + s]:
                maximum += 1
            radii[s][i] = maximum
            k = 1
            while radii[s][i - k] != (maximum - k) and k < maximum:
                radii[s][i + k] = min(radii[s][i - k], maximum - k)
                k += 1
            maximum = max(maximum - k, 0)
            i += k

    return radii


# =============================================================================
# MAIN
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    N = int(input())
    S = input()
    time_a = time.time()
    all_palindromes(S, N)
    time_b = time.time()
    print("time: {} secs".format(round(time_b - time_a, 3)))


# =============================================================================
# TESTS
# -----------------------------------------------------------------------------
def test_all_palindromes():
    word = "happytotwilling"
    radii = all_palindromes(word, len(word))
    palindromes = sorted(
        word[i - 1 - m : i - 1 + m + s]
        for s, r in enumerate(radii)
        for i, m in enumerate(r)
        if m > 0
    )
    assert palindromes == ["illi", "pp", "tot"]
