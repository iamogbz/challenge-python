# A DashMart is a warehouse run by DoorDash that houses items found in convenience stores, grocery stores, and restaurants. We have a city with open roads, blocked-off roads, and DashMarts.

# City planners want you to identify how far a location is from its closest DashMart.

# You can only travel over open roads (up, down, left, right).

# Locations are given in [row, col] format.

import math

# Example 1
example_map = [
    #     0    1    2    3    4    5    6    7    8
    ["X", " ", " ", "D", " ", " ", "X", " ", "X"],  # 0
    ["X", " ", "X", "X", " ", " ", " ", " ", "X"],  # 1
    [" ", " ", " ", "D", "X", "X", " ", "X", " "],  # 2
    [" ", " ", " ", "D", " ", "X", " ", " ", " "],  # 3
    [" ", " ", " ", " ", " ", "X", " ", " ", "X"],  # 4
    [" ", " ", " ", " ", "X", " ", " ", "X", "X"],  # 5
]

# ' ' represents an open road that you can travel over in any direction (up, down, left, or right).
# 'X' represents an blocked road that you cannot travel through.
# 'D' represents a DashMart.

# # list of pairs [row, col]
locations = [[200, 200], [1, 4], [0, 3], [5, 8], [1, 8], [5, 5]]

# answer = [-1, 2, 0, -1, 6, 9]

# Provided:
# - city: char[][]
# - locations: int[][2]

# Return:
# - answer: int[]
# Return a list of the distances from a given point to its closest DashMart.

# Expected Answer: In this case, you should return [-1, 2, 0, -1, 6, 9].

OPEN_PATH = " "
DOOR_DASH_WH = "D"
BLOCKED_PATH = "X"


def min_distance_to_loc(
    current_location: "tuple[int, int]",
    distance_so_far,
    target_location,
    grid,
    visited_locations: "set[tuple[int, int]]",
) -> "int":
    max_row = len(grid)
    max_col = len(grid[0])

    visited_locations = set([*visited_locations, current_location])

    # print("min distance to:", current_location, target_location, distance_so_far, visited_locations)

    if current_location == target_location:
        return distance_so_far

    # get all the next moves from th ecurrent location
    next_steps = [
        (current_location[0] - 1, current_location[1]),
        (current_location[0], current_location[1] - 1),
        (current_location[0] + 1, current_location[1]),
        (current_location[0], current_location[1] + 1),
    ]

    # ensure all the next steps can be traversed and has not been visited before
    valid_next_steps = [
        step
        for step in next_steps
        if step[0] >= 0
        and step[0] < max_row
        and step[1] >= 0
        and step[1] < max_col
        and grid[step[0]][step[1]] != BLOCKED_PATH
        and step not in visited_locations
    ]

    results = [
        min_distance_to_loc(
            step, distance_so_far + 1, target_location, grid, visited_locations
        )
        for step in valid_next_steps
    ]

    if not results:
        return math.inf

    return min(results)


def find_closest_dd_warehouse(
    start_location: "list[int, int]", grid: "list[int][int]"
) -> "int":
    """note to self lookup shortest path algo"""
    """walks the entire map and returns the closest dd warehouse"""

    dd_warehouses = [
        (rowIdx, colIdx)
        for (rowIdx, column) in enumerate(grid)
        for (colIdx, value) in enumerate(column)
        if value == DOOR_DASH_WH
    ]

    # print(dd_warehouses)

    # option sort by heuristic of index difference with start location
    results = [
        min_distance_to_loc(start_location, 0, dd_warehouse, grid, set())
        for dd_warehouse in dd_warehouses
    ]

    # print("combined results:", results)

    return min([-1 if dist == math.inf else dist for dist in results])


def main():
    results = [
        find_closest_dd_warehouse((row, col), example_map) for [row, col] in locations
    ]
    print(results)


main()
