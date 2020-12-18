#!/usr/bin/env python3

import copy

import pytest

directions = (
    (-1, -1, -1),  # 1 below
    (-1, -1, 0),   # 1 below
    (-1, -1, +1),  # 1 below
    (-1, 0, -1),   # 1 below
    (-1, 0, 0),    # 1 below
    (-1, 0, +1),   # 1 below
    (-1, +1, -1),  # 1 below
    (-1, +1, 0),   # 1 below
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
    (+1, -1, 0),   # 1 above
    (+1, -1, +1),  # 1 above
    (+1, 0, -1),   # 1 above
    (+1, 0, 0),    # 1 above
    (+1, 0, +1),   # 1 above
    (+1, +1, -1),  # 1 above
    (+1, +1, 0),   # 1 above
    (+1, +1, +1),  # 1 above
)

ACTIVE = "#"
INACTIVE = "."


def next_state(coords, grid):
    x, y, z = coords
    occupied_neighbors = 0
    current_state = grid.get((x, y, z))
    for direction in directions:
        delta_x, delta_y, delta_z = direction
        new_x, new_y, new_z = x + delta_x, y + delta_y, z + delta_z
        neighbor_state = grid.get((new_x, new_y, new_z), INACTIVE)
        occupied_neighbors += neighbor_state == ACTIVE

    if current_state == ACTIVE:
        if 2 <= occupied_neighbors <= 3:
            return ACTIVE
        else:
            return INACTIVE
    elif current_state == INACTIVE:
        if occupied_neighbors == 3:
            return ACTIVE
        else:
            return INACTIVE


def evolve_grid(grid):
    next_grid = copy.copy(grid)
    for x, y, z in grid.keys():
        for dx, dy, dz in directions:
            new_x, new_y, new_z = x + dx, y + dy, z + dz
            neighbor_coords = (new_x, new_y, new_z)
            if neighbor_coords not in grid:
                next_grid[neighbor_coords] = INACTIVE
    for coords in next_grid:
        next_grid[coords] = next_state(coords, next_grid)
    return next_grid


def print_grid(grid):
    min_x, min_y, min_z = 0, 0, 0
    max_x, max_y, max_z = 0, 0, 0
    for x, y, z in grid.keys():
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        min_z = min(min_z, z)
        max_z = max(max_z, z)

    for z in range(min_z, max_z+1):
        for y in range(min_y, max_y+1):
            print("".join([grid.get((x, y, z), INACTIVE) for x in range(min_x, max_x+1)]))


def part_one(grid, cycles=6):
    print("Entry")
    print_grid(grid)
    print("Loop")
    for _i in range(cycles+1):
        grid = evolve_grid(grid)
        #print("#"*80)
        #print_grid(grid)

    active = 0
    for value in grid.values():
        active += value == ACTIVE
    print(active)
    return active


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {
                (1, 0, 0): ACTIVE,
                (2, 1, 0): ACTIVE,
                (0, 2, 0): ACTIVE,
                (1, 2, 0): ACTIVE,
                (2, 2, 0): ACTIVE,
            },
            112,
        ),
    ],
)
def test_part_one(input, expected):
    assert part_one(input) == expected


@pytest.mark.parametrize(
    "grid, coords, expected",
    [
        (
            {
                (1, 0, 0): ACTIVE,
                (2, 1, 0): ACTIVE,
                (0, 2, 0): ACTIVE,
                (1, 2, 0): ACTIVE,
                (2, 2, 0): ACTIVE,
            },
                (1,2,0),
                ACTIVE,
        ),
    ],
)
def test_next_state(grid, coords, expected):
    assert next_state(coords, grid) == expected
