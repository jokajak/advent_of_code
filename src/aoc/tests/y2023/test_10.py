#!/usr/bin/env python
"""Tests for AoC 10, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d10 import parse, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=10)
    return puzzle.examples[0].input_data


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = None
    ret = parse(example_data)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 4
    ret = solve_part_one(parse(example_data), start_coordinate=(1, 1))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


@pytest.mark.parametrize(
    "example_data, expected",
    [
        (
            """....
.S7.
.LJ.
....""",
            0,
        ),
        (
            """....
.S7.
.||.
.LJ.
....""",
            0,
        ),
        (
            """....
.S-7.
.|.|.
.L-J.
....""",
            1,
        ),
        (
            """.....
.S--7.
.|..|.
.L--J.
.....""",
            2,
        ),
        (
            """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
""",
            4,
        ),
        (
            """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7OF-J|.
.|..|O|..|.
.L--JOL--J.
.....O.....""",
            4,
        ),
        (
            """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""",
            8,
        ),
    ],
)
def test_part2(example_data, expected):
    """Test part 2 on example input"""
    ret = solve_part_two(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected
