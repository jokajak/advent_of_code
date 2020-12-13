#!/usr/bin/env python


__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse
from collections import Counter

import pytest


def part_one(inputs):
    """Calculate manhattan units for ship movements

    Args:
        inputs (list): List of movement instructions
    """
    direction = "E"
    rotations = list("NESW")
    x, y = 0, 0
    for movement in inputs:
        action, value = movement[0], int(movement[1:])
        index_change = int(value / 90)
        current_index = rotations.index(direction)
        if action == "F":
            if direction == "E":
                x += value
            elif direction == "W":
                x -= value
            elif direction == "N":
                y += value
            elif direction == "S":
                y -= value
        elif action == "N":
            y += value
        elif action == "S":
            y -= value
        elif action == "W":
            x -= value
        elif action == "E":
            x += value
        elif action == "R":
            direction = rotations[(current_index + index_change) % 4]
        elif action == "L":
            direction = rotations[(current_index - index_change) % 4]
    return (direction, x, y)


def part_two(inputs):
    """Calculate manhattan units for ship movements

    Args:
        inputs (list): List of movement instructions
    """
    direction = "E"
    x, y = 0, 0
    waypoint_x_delta, waypoint_y_delta = 10, 1
    for movement in inputs:
        action, value = movement[0], int(movement[1:])
        index_change = int(value / 90)
        if action == "F":
            x += value * waypoint_x_delta
            y += value * waypoint_y_delta
        elif action == "N":
            waypoint_y_delta += value
        elif action == "S":
            waypoint_y_delta -= value
        elif action == "W":
            waypoint_x_delta -= value
        elif action == "E":
            waypoint_x_delta += value
        elif action == "R":
            for _rotate in range(index_change, 0, -1):
                waypoint_x_delta, waypoint_y_delta = waypoint_y_delta, -waypoint_x_delta
        elif action == "L":
            for _rotate in range(index_change, 0, -1):
                waypoint_x_delta, waypoint_y_delta = -waypoint_y_delta, waypoint_x_delta
    return (direction, x, y)


def main(args):
    """Main program flow

    Args:
        args (argparse.Namespace): Parsed arguments
    """
    directions = []
    for line in args.file.readlines():
        line = line.strip("\n")
        directions.append(line)

    direction, x, y = part_one(directions)
    print(abs(x)+abs(y))
    direction, x, y = part_two(directions)
    print(abs(x)+abs(y))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument(
        "--file",
        type=argparse.FileType("r"),
        help="Input file",
        default="2020/inputs/day_12/test.txt",
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)


# TESTS


@pytest.mark.parametrize(
    "input, expected",
    [
        (("N", "R90"), "E"),
        (("N", "R270"), "W"),
    ],
)
def test_split_range(input, expected):
    direction, movement = input
    action, value = movement[0], int(movement[1:])
    rotations = list("NESW")
    index_change = int(value / 90)
    current_index = rotations.index(direction)
    if action == "R":
        new_index = rotations[(current_index + index_change) % 4]
    elif action == "L":
        new_index = rotations[(current_index - index_change) % 4]
    assert new_index == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            [
                "F10",
                "N3",
                "F7",
                "R90",
                "F11",
            ],
            25,
        )
    ],
)
def test_part_one(input, expected):
    direction, x, y = part_one(input)
    assert abs(x)+abs(y) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (((10, 4), "R90"), (4, -10)),
        (((4, -10), "R90"), (-10, -4)),
        (((-10, -4), "R90"), (-4, 10)),
        (((-4, 10), "R90"), (10, 4)),
        (((10, 4), "R180"), (-10, -4)),
        (((10, 4), "R270"), (-4, 10)),
        (((10, 4), "L90"), (-4, 10)),
        (((10, 4), "L180"), (-10, -4)),
        (((10, 4), "L270"), (4, -10)),
    ],
)
def test_rotate_waypoint(input, expected):
    current_waypoint, movement = input
    waypoint_x_delta, waypoint_y_delta = current_waypoint
    action, value = movement[0], int(movement[1:])
    index_change = int(value / 90)
    if index_change == 2:
        waypoint_x_delta, waypoint_y_delta = -waypoint_x_delta, -waypoint_y_delta
    elif action == "R":
        for _rotate in range(index_change, 0, -1):
            waypoint_x_delta, waypoint_y_delta = waypoint_y_delta, -waypoint_x_delta
    elif action == "L":
        for _rotate in range(index_change, 0, -1):
            waypoint_x_delta, waypoint_y_delta = -waypoint_y_delta, waypoint_x_delta
    assert (waypoint_x_delta, waypoint_y_delta) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            [
                "F10",
                "N3",
                "F7",
                "R90",
                "F11",
            ],
            286,
        )
    ],
)
def test_part_two(input, expected):
    direction, x, y = part_two(input)
    assert abs(x)+abs(y) == expected
