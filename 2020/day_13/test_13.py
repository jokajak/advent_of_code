#!/usr/bin/env python


__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse
import math
from itertools import count

import pytest


def part_one(arrival_time, bus_routes):
    closest_route, closest_time = 0, 9999
    for bus_route in bus_routes:
        if bus_route == "x":
            continue
        bus_route = int(bus_route)
        closest_arrival = math.ceil(arrival_time / bus_route) * bus_route
        if (closest_arrival - arrival_time) < closest_time:
            closest_route = bus_route
            closest_time = closest_arrival - arrival_time
    return closest_route


def lcm(a, b):
    return a*b // math.gcd(a, b)


def part_two(bus_routes):
    # for each bus number, find the lcm of the next bus
    buses = []
    for i, v in enumerate(bus_routes):
        if v == 'x':
            continue
        buses.append((i, int(v)))

    # current time stamp, current period of each step
    t, step = buses[0]
    # for each bus number, find the lcm of the current step and the bus number
    for delta, period in buses[1:]:
        for t in count(t, step):
            if (t + delta) % period == 0:
                break
        # update the step size to ensure it includes previous findings
        step = lcm(step, period)
    return t


def main(args):
    """Main program flow

    Args:
        args (argparse.Namespace): Parsed arguments
    """
    inputs = []
    for line in args.file.readlines():
        line = line.strip("\n")
        inputs.append(line)
    arrival_time = int(inputs[0])
    bus_routes = inputs[1].split(",")
    closest_route = part_one(arrival_time, bus_routes)
    time_delta = math.ceil(arrival_time / closest_route)*closest_route - arrival_time
    print(closest_route*time_delta)
    print(part_two(bus_routes))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument(
        "--file",
        type=argparse.FileType("r"),
        help="Input file",
        default="2020/inputs/5",
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
        ((939, [7, 13, "x", "x", 59, "x", 31, 19]), 59),
    ],
)
def test_part_one(input, expected):
    arrival_time, bus_routes = input
    assert part_one(arrival_time, bus_routes) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ([7, 13, "x", "x", 59, "x", 31, 19], 1068781),
    ],
)
def test_part_two(input, expected):
    assert part_two(input) == expected
