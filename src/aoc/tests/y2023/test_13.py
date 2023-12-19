#!/usr/bin/env python
"""Tests for AoC 13, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d13 import (
    Graph,
    get_horizontal_middle,
    parse,
    solve_part_one,
    solve_part_two,
)


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=13)
    return puzzle.examples[0].input_data


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = None
    ret = parse(example_data)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [
        (
            """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""",
            3,
        )
    ],
)
def test_get_horizontal_middle(input_data, expected):
    middle = get_horizontal_middle(parse(input_data)[0])
    assert middle == expected


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 405
    ret = solve_part_one(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = None
    ret = solve_part_two(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected
