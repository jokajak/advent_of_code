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
    ],
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


def should_flip(*, black_tiles, coordinate):
    x, y = coordinate
    black_neighbors = 0
    ret = False
    for direction in DIRECTIONS:
        delta_x, delta_y = DIRECTIONS[direction]
        new_coord = (x + delta_x, y + delta_y)
        if new_coord in black_tiles:
            black_neighbors += 1
    if coordinate in black_tiles:
        if black_neighbors == 0 or black_neighbors > 2:
            ret = True
    else:
        if black_neighbors == 2:
            ret = True
    return ret


def flip_tiles(black_tiles):
    # any black tile with zero or more than 2 black tiles immediately adjacent flip to white
    # any white tile with exactly 2 black tiles immediately adjacent flip to black
    adjacent_coords = [
        (+1, -1),
        (+2, 0),
        (+1, +1),
        (-1, +1),
        (-2, 0),
        (-1, -1),
    ]
    new_tiles = set()
    for tile in black_tiles:
        x, y = tile
        for dx, dy in adjacent_coords:
            coord = (x + dx, y + dy)
            should_tile_flip = should_flip(black_tiles=black_tiles, coordinate=coord)
            if coord in black_tiles and not should_tile_flip:
                new_tiles.add(coord)
            elif coord not in black_tiles and should_tile_flip:
                new_tiles.add(coord)
    return new_tiles


def main():
    lines = []
    with open("input.txt", "r") as f:
        for line in f.readlines():
            lines.append(line.strip("\n"))

    black_tiles = set()
    for line in lines:
        coordinate = get_coordinate(line)
        if coordinate in black_tiles:
            black_tiles.remove(coordinate)
        else:
            black_tiles.add(coordinate)
    print("Part 1: ", len(black_tiles))

    for _ in tqdm.tqdm(range(100)):
        black_tiles = flip_tiles(black_tiles)

    print("Part 2: ", len(black_tiles))



if __name__ == "__main__":
    main()
