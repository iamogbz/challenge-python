"""
https://www.hackerrank.com/challenges/crush/problem
"""

import bisect
import functools
import math
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


class SpanSums:
    """Class to track and update values at given span ranges"""

    __entries = []  # map of span node to value
    __max_value = 0

    def __repr__(self) -> str:
        entry_count = len(self.__entries)
        view_count = 1
        return f"{dict(self.__entries[:view_count])}(+{entry_count - view_count})"

    def overlaps(self, span_a: "tuple[int, int]", span_b: "tuple[int, int]"):
        span_a_inside_span_b = span_a[0] >= span_b[0] and span_a[0] <= span_b[1]
        span_b_inside_span_a = span_b[0] >= span_a[0] and span_b[0] <= span_a[1]
        return span_a_inside_span_b or span_b_inside_span_a

    def split_merge(
        self,
        span_a_v: "tuple[tuple[int, int], int]",
        span_b_v: "tuple[tuple[int, int], int]",
    ):
        (span_i, value_i), (span_j, value_j) = sorted([span_a_v, span_b_v])
        span_x = (span_i[0], max(span_i[0], span_j[0]) - 1)
        span_y = (span_x[1] + 1, min(span_i[1], span_j[1]))
        span_z = (span_y[1] + 1, max(span_i[1], span_j[1]))
        span_vs = (
            (span_x, value_i),
            (span_y, value_i + value_j),
            (span_z, value_i if span_i[1] > span_j[1] else value_j),
        )
        return tuple(
            span_v if span_v[0][0] <= span_v[0][1] else None for span_v in span_vs
        )

    @timeit
    def insert(self, v: "tuple[tuple[int, int], int]"):
        """Add span value to sorted entries and update max value"""
        if v is not None:
            bisect.insort(self.__entries, v)
            if v[1] > self.__max_value:
                self.__max_value = v[1]

    @timeit
    def add_span_value(self, span_inc: "tuple[int, int]", value: "int"):
        """Add span value to entries updating any overlapping spans"""
        left_idx = max(
            0, bisect.bisect_left(self.__entries, ((span_inc[0], 0), None)) - 1
        )
        right_idx = bisect.bisect_right(self.__entries, ((span_inc[1], math.inf), None))
        # print(
        #     f"[Insert]: {(span_inc, value)}",
        #     f"[Update]: [{left_idx}:{right_idx}]",
        # )

        pop_offset = 0
        # identify and remove now obsolete spans from existing entries
        for _ in range(left_idx, right_idx):
            span, existing_value = self.__entries.pop(left_idx + pop_offset)
            span_intersect = (max(span[0], span_inc[0]), min(span[1], span_inc[1]))
            # print("[Split]", span, span_intersect)
            for span_v in self.split_merge(
                (span, existing_value), (span_intersect, value)
            ):
                if span_v is not None:
                    pop_offset += 1
                    self.insert(span_v)

        # if no existing spans then just add new value to sorted entries
        if left_idx == right_idx:
            self.insert((span_inc, value))

        # print("current", self)

    @property
    def max_value(self):
        """Return the max span sum value"""
        return self.__max_value


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
    span_sums = SpanSums()
    span_sums.add_span_value((1, array_size), 0)

    for _ in range(query_count):
        span_min, span_max, value = read_line_as_int_values()
        span_sums.add_span_value((span_min, span_max), value)
        # print("---")

    print(span_sums.max_value)


main()
