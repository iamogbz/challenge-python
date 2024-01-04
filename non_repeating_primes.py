"""
Efficiently get all the primes of a specific digit length
"""

from typing import Iterator, List


def main():
    num_digits = capture_num_digits()
    print(primes_of_length(num_digits))


def capture_num_digits() -> int:
    num_digits = None

    while num_digits == None:
        try:
            n = input("Enter the number of digits in the prime number: ")
            num_digits = int(n)
        except:
            print(f"Invalid number entered '{n}', please try again.")

    return num_digits


def primes_of_length(length: int) -> List[int]:
    min_num = pow(10, length - 1)
    max_num = min_num * 10
    list_of_primes = primes_between(min_num, max_num)
    return sorted(list_of_primes, key=prime_sort_key)


def prime_sort_key(p: int) -> str:
    """
    Returns a sort key based on the number of unique digits then the prime value
    """
    digit_count = len(str(p))
    unique_digit_count = len(set(str(p)))
    unique_digit_key = digit_count - unique_digit_count
    return f"{unique_digit_key}_{p}"


def primes_between(min_n: int, max_n: int) -> Iterator[int]:
    for n in range(min_n, max_n):
        if is_prime(n):
            yield n


def is_prime(n: int) -> bool:
    for i in range(2, n):
        if n % i == 0:
            return False
    return n > 1


main()
