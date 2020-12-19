#!/usr/bin/env python3

import copy
from operator import itemgetter
from itertools import product

import pytest

directions = (
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

ACTIVE = "#"
INACTIVE = "."


# def alive_neighbors(grid, x, y, z):
    # occupied_neighbors = 0
    # for direction in directions:
        # delta_x, delta_y, delta_z = direction
        # new_x, new_y, new_z = x + delta_x, y + delta_y, z + delta_z
        # if (new_x, new_y, new_z) in grid:
            # occupied_neighbors += 1
    # return occupied_neighbors


def alive_neighbors(cube, coords):
    ranges = ((c - 1, c, c + 1) for c in coords)
    alive = sum(p in cube for p in product(*ranges))
    alive -= coords in cube
    return alive


def next_state(coords, grid):
    x, y, z = coords
    if (x, y, z) in grid:
        current_state = ACTIVE
    else:
        current_state = INACTIVE
    occupied_neighbors = alive_neighbors(grid, coords)
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


# From https://github.com/mebeim/aoc/tree/master/2020#day-17---conway-cubes
#def bounds(cube):
#    # iterate over 3 dimensions
#    for i in range(3):
#        # get the minimum value from
#        lo = min(map(itemgetter(i), cube)) - 1
#        hi = min(map(itemgetter(i), cube)) + 2
#        yield range(lo, hi)
def bounds(cube, n_dims=3):
    for i in range(n_dims):
        lo = min(map(itemgetter(i), cube)) - 1
        hi = max(map(itemgetter(i), cube)) + 2
        yield range(lo, hi)
#
#
#def evolve(cube):
#    new = set()
#
#    for coords in product(*bounds(cube)):
#        # coords is (x, y, z)
#        alive = alive_neighbors(cube, coords)
#
#        # Simplified conditions from above
#        if (coords in cube and alive in (2, 3)) or alive == 3:
#            new.add(coords)
#
#    return new



def evolve(cube, n_dims=3):
    new = set()

    for coord in product(*bounds(cube, n_dims)):
        alive = alive_neighbors(cube, coord)
        if (coord in cube and alive in (2, 3)) or alive == 3:
            new.add(coord)

    return new


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

    for z in range(min_z, max_z + 1):
        for y in range(min_y, max_y + 1):
            print(
                "".join(
                    [grid.get((x, y, z), INACTIVE) for x in range(min_x, max_x + 1)]
                )
            )


def part_one(grid, cycles=6, n_dims=3):
    #    print("Entry")
    #    print_grid(grid)
    #    print("Loop")
    #    for _i in range(cycles+1):
    #        grid = evolve_grid(grid)
    #        #print("#"*80)
    #        #print_grid(grid)
    #
    #    active = 0
    #    for value in grid.values():
    #        active += value == ACTIVE
    #    print(active)
    #    return active
    cube = {coord for coord in grid}
    for _ in range(cycles):
        if cube is not None:
            cube = evolve(cube)

    total_alive = len(cube)
    print("Part 1:", total_alive)


def part_two(grid):
    cube = {coord for coord in grid}
    for _ in range(6):
        if cube is not None:
            cube = evolve(cube, n_dims=4)

    total_alive = len(cube)
    print("Part 2:", total_alive)


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
                (1, 0, 0),
                (2, 1, 0),
                (0, 2, 0),
                (1, 2, 0),
                (2, 2, 0),
            },
            (1, 2, 0),
            ACTIVE,
        ),
    ],
)
def test_next_state(grid, coords, expected):
    assert next_state(coords, grid) == expected


@pytest.mark.parametrize(
    "grid, coords, expected",
    [
        (
            {
                (1, 0, 0),
                (2, 1, 0),
                (0, 2, 0),
                (1, 2, 0),
                (2, 2, 0),
            },
            (1, 2, 0),
            3,
        ),
        (
            {
                (1, 0, 0),
                (2, 1, 0),
                (0, 2, 0),
                (1, 2, 0),
                (2, 2, 0),
            },
            (2, 2, 0),
            2,
        ),
        (
            {
                (1, 0, 0),
                (2, 1, 0),
                (0, 2, 0),
                (1, 2, 0),
                (2, 2, 0),
            },
            (1, 3, 0),
            3,
        ),
    ],
)
def test_alive_neighbors(grid, coords, expected):
    assert alive_neighbors(grid, coords) == expected


def main():
    inputs = []
    with open("input.txt") as f:
        for line in f.readlines():
            line = line.strip("\n")
            inputs.append(line)

    grid = set()
    for y, line in enumerate(inputs):
        for x, val in enumerate(list(line)):
            if val == ACTIVE:
                grid.add((x, y, 0))
    part_one(grid)
    grid = set()
    for y, line in enumerate(inputs):
        for x, val in enumerate(list(line)):
            if val == ACTIVE:
                grid.add((x, y, 0, 0))
    part_two(grid)


if __name__ == "__main__":
    main()
