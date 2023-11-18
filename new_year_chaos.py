"""https://www.hackerrank.com/challenges/new-year-chaos/problem"""

BRIBE_LIMIT = 2


def bubble_sort(q):
    """Swap in place bubble sort"""
    n = len(q)
    in_swap = False
    total_swap_count = 0
    value_swap_counts = {}
    max_value_swap_count = 0
    for i in range(n):
        for j in range(n - i - 1):
            in_swap = q[j] > q[j + 1]
            # print(q[j:j+2])
            if in_swap:
                # count the swap
                if q[j] not in value_swap_counts:
                    value_swap_counts[q[j]] = 0
                value_swap_counts[q[j]] += 1
                if value_swap_counts[q[j]] > max_value_swap_count:
                    max_value_swap_count = value_swap_counts[q[j]]
                # if max_value_swap_count > BRIBE_LIMIT:
                # return max_value_swap_count, total_swap_count
                total_swap_count += 1
                # do the swap
                q[j], q[j + 1] = q[j + 1], q[j]
                print(q)
        # If no two elements were swapped
        # there is a bug here
        # if not in_swap:
        #     break

    # print(value_swap_counts)
    # value_counts = value_swap_counts.values()
    # return max(value_counts), sum(value_counts)
    return max_value_swap_count, total_swap_count


def bubble_sort_count(q):
    """Count swaps needed without performing them"""
    queue_size = len(q)
    total_swap_count = 0
    max_value_swap_count = 0

    # starting from the last place in the queue
    min_orig_pos_seen = queue_size
    for curr_pos in range(queue_size, 0, -1):
        orig_pos = q[curr_pos - 1]  # the values are the original places in queue

        if orig_pos > curr_pos:
            swaps_needed = orig_pos - curr_pos
            total_swap_count += swaps_needed
            if swaps_needed > max_value_swap_count:
                max_value_swap_count = swaps_needed
        else:
            if min_orig_pos_seen > orig_pos:
                min_orig_pos_seen = orig_pos
            elif min_orig_pos_seen != orig_pos:
                total_swap_count += 1

        print([min_orig_pos_seen, curr_pos, [orig_pos], total_swap_count])

        # if max_value_swap_count > BRIBE_LIMIT:
        #     break

    return max_value_swap_count, total_swap_count


def test_adjacent_swap_count():
    """Validate test cases"""
    test_cases = [
        ([2, 1, 5, 3, 4], 3, 2),
        ([2, 5, 1, 3, 4], 4, 3),
        ([5, 1, 2, 3, 7, 8, 6, 4], 9, 4),
        ([1, 2, 5, 3, 7, 8, 6, 4], 7, 2),
        ([3, 5, 2, 1, 4], 6, 3),
        ([4, 1, 2, 3], 3, 3),
    ]
    for tc, expected_count, single_count in test_cases:
        print([[tc]])
        max_count, swap_count = bubble_sort_count(tc)
        try:
            assert swap_count == expected_count
            print("Assertion! swap passed: ", swap_count)
        except AssertionError:
            print(
                "Assertion! swap actual: ", swap_count, " <> expected: ", expected_count
            )
        try:
            assert max_count == single_count
            print("Assertion! sngl passed: ", max_count)
        except AssertionError:
            print("Assertion! sngl actual: ", max_count, " <> expected: ", single_count)


test_adjacent_swap_count()
