"""
https://www.hackerrank.com/challenges/crush/problem
"""

import functools
import time


def timeit(func):
    """Function decorator to print execution time in seconds"""
    threshold_s = 0.05

    @functools.wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        if total_time >= threshold_s:
            print(
                f"[Function] {func.__name__}{args} {kwargs}",
                f"Took {total_time:.4f} seconds",
            )
        return result

    return timeit_wrapper


def read_line_as_int_values():
    """Read the input line as space delimited integers"""
    return [int(n) for n in input().split()]


@timeit
def main():
    """
    Run main code
    for each range given add mapping of range to union for value
      keeping track of the maximum value at anytime
    """
    if __name__ != "__main__":
        return

    array_size, query_count = read_line_as_int_values()
    range_union = {}

    for _ in range(query_count):
        range_min, range_max, value = read_line_as_int_values()
        range_union[range_min] = range_union.get(range_min, 0) + value
        range_union[range_max + 1] = range_union.get(range_max + 1, 0) - value

    cumm_sum = 0
    max_value = 0
    for i in range(array_size + 1):
        cumm_sum += range_union.get(i, 0)
        if cumm_sum > max_value:
            max_value = cumm_sum

    print(max_value)


main()
