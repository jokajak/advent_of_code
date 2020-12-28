#!/usr/bin/env python

import pytest
import tqdm

# Using doubled coordinate system from https://www.redblobgames.com/grids/hexagons/

DIRECTIONS = {
    "ne": (+1, -1),
    "e": (+2, 0),
    "se": (+1, +1),
    "sw": (-1, +1),
    "w": (-2, 0),
    "nw": (-1, -1),
}


@pytest.mark.parametrize(
    "input, expected",
    [
        ("esew", (1, 1)),
        ("nwwswee", (0, 0)),
    ]
)
def test_get_coordinate(input, expected):
    assert get_coordinate(input) == expected


def get_next_direction(id):
    if id[0] == "s" or id[0] == "n":
        return id[0:2]
    else:
        return id[0]


def get_coordinate(id):
    directions = list(id)
    coordinate = (0, 0)
    while len(directions) > 0:
        if directions[0] == "s" or directions[0] == "n":
            direction = directions[0:2]
            del directions[0:2]
        else:
            direction = directions.pop(0)
        delta_x, delta_y = DIRECTIONS["".join(direction)]
        x, y = coordinate
        coordinate = (x + delta_x, y + delta_y)
    return coordinate


def main():
    lines = []
    with open("input.txt", "r") as f:
        for line in f.readlines():
            lines.append(line.strip("\n"))

    black_tiles = set()
    for line in tqdm.tqdm(lines):
        coordinate = get_coordinate(line)
        if coordinate in black_tiles:
            black_tiles.remove(coordinate)
        else:
            black_tiles.add(coordinate)
    print("Part 1: ", len(black_tiles))


if __name__ == "__main__":
    main()
