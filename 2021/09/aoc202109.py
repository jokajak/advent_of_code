"""AoC 9, 2021"""

# Standard library imports
import pathlib
import sys
import math
from itertools import product
from collections import deque
from aocd import data as input_data, submit

directions_3d = (
    (-1, -1, -1),  # 1 below
    (-1, -1, 0),  # 1 below
    (-1, -1, +1),  # 1 below
    (-1, 0, -1),  # 1 below
    (-1, 0, 0),  # 1 below
    (-1, 0, +1),  # 1 below
    (-1, +1, -1),  # 1 below
    (-1, +1, 0),  # 1 below
    (-1, +1, +1),  # 1 below
    (0, -1, -1),
    (0, -1, 0),
    (0, -1, +1),
    (0, 0, -1),
    (0, 0, +1),
    (0, +1, -1),
    (0, +1, 0),
    (0, +1, +1),
    (+1, -1, -1),  # 1 above
    (+1, -1, 0),  # 1 above
    (+1, -1, +1),  # 1 above
    (+1, 0, -1),  # 1 above
    (+1, 0, 0),  # 1 above
    (+1, 0, +1),  # 1 above
    (+1, +1, -1),  # 1 above
    (+1, +1, 0),  # 1 above
    (+1, +1, +1),  # 1 above
)

# delta_x, delta_y
directions_2d = (
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)


def parse(puzzle_input):
    """Parse input"""
    puzzle_input = puzzle_input.splitlines()
    grid = []
    for row, entries in enumerate(puzzle_input):
        new_row = []
        for col, value in enumerate(entries):
            new_row.append(int(value))
        grid.append(new_row)
    return grid


def get_neighbors(grid: list, coords: set) -> list:
    neighbor_vals = []
    row, col = coords
    for direction in directions_2d:
        delta_x, delta_y = direction
        neighbor_row = row + delta_y
        neighbor_col = col + delta_x
        # we know that the column is within the grid
        if 0 <= neighbor_row < len(grid):
            if 0 <= neighbor_col < len(grid[neighbor_row]):
                neighbor_vals.append(grid[neighbor_row][neighbor_col])
    assert 2 <= len(neighbor_vals) <= 4
    return neighbor_vals


def part1(data):
    """Solve part 1"""
    total_risk = 0
    for row, entries in enumerate(data):
        for col, value in enumerate(entries):
            value = int(value)
            neighbors = get_neighbors(data, (row, col))
            if min(neighbors) > value:
                risk_level = value + 1
                total_risk += risk_level
    return total_risk


def get_basin_size(grid: list, coords: set) -> int:
    """Calculate a basin size.

    Given a grid and coordinates, find all coordinates around the provided coordinates that are less than 9

    From https://en.wikipedia.org/wiki/Flood_fill
    """
    basin_entries = deque()
    unmapped_entries = deque()
    unmapped_entries.append(coords)
    while len(unmapped_entries) > 0:
        row, col = coords = unmapped_entries.pop()
        if grid[row][col] == 9 or coords in basin_entries:
            continue
        basin_entries.append(coords)
        for direction in directions_2d:
            delta_x, delta_y = direction
            neighbor_row = row + delta_y
            neighbor_col = col + delta_x
            # we know that the column is within the grid
            if (0 <= neighbor_row < len(grid)) and 0 <= neighbor_col < len(
                grid[neighbor_row]
            ):
                unmapped_entries.append((neighbor_row, neighbor_col))

    # look left first
    return basin_entries


def part2(data):
    """Solve part 2.

    Next, you need to find the largest basins so you know what areas are most important to avoid.

    A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a
    basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other
    locations will always be part of exactly one basin.

    The size of a basin is the number of locations within the basin, including the low point. The example above has four
    basins.
    """
    basins = []
    for row, entries in enumerate(data):
        for col, value in enumerate(entries):
            value = int(value)
            neighbors = get_neighbors(data, (row, col))
            if min(neighbors) > value:
                # we've found a basin
                basin_size = get_basin_size(data, (row, col))
                basins.append(len(basin_size))
    basins = sorted(basins)
    return math.prod(basins[-3:])


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    answer_a, answer_b = solve(puzzle_input=input_data)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
