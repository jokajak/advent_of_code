#!/usr/bin/env python
"""Solutions for AoC 14, 2023."""
# Created: 2023-12-15 08:03:09.032874

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from collections import defaultdict


def parse(input_data):
    """Transform the data.

    O....#....
    O.OO#....#
    .....##...
    OO.#O....O
    .O.....O#.
    O.#..O.#.#
    ..O..#O..O
    .......O..
    #....###..
    #OO..#....
    """
    reversed_graph = defaultdict(dict)
    for line in input_data.split():
        for col_index, char in enumerate(line):
            if char == ".":
                continue
            reversed_graph[]
    return input_data


def get_load(graph):
    """Calculate the load.

    The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south
    edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the
    amount of load caused by each rock in each row is as follows:

    OOOO.#.O.. 10
    OO..#....#  9
    OO..O##..O  8
    O..#.OO...  7
    ........#.  6
    ..#....#.#  5
    ..O..#.O.O  4
    ..O.......  3
    #....###..  2
    #....#....  1

    The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.
    """

    ret = 0
    for row_index, row in enumerate(graph):
        for column in row:
            if column == "O":
                ret += row_index + 1
    return ret


def solve_part_one(input_data):
    """Solve part one.

    Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support
    beams?
    """
    answer = None
    return answer


def solve_part_two(input_data):
    """Solve part two."""
    answer = None
    return answer


def main():
    puzzle = Puzzle(year=2023, day=14)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 14), {})
    if stats.get("a", None) is None:
        answer_a = solve_part_one(parsed_data)
        if answer_a:
            puzzle.answer_a = answer_a
    if stats.get("b", None) is None:
        parsed_data = parse(puzzle.input_data)
        answer_b = solve_part_two(parsed_data)
        if answer_b:
            puzzle.answer_b = answer_b


if __name__ == "__main__":
    main()
