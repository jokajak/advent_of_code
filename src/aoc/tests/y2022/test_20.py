#!/usr/bin/env python
"""Tests for AoC 20, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d20 import Msg, parse, rearrange, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=20)
    return puzzle.example_data


@pytest.mark.parametrize(
    "current, instruction, expected",
    [
        (([4, 5, 6, 1, 7, 8, 9], 1, [4, 5, 6, 7, 1, 8, 9])),
        (([4, -2, 5, 6, 7, 8, 9], -2, [4, 5, 6, 7, 8, -2, 9])),
    ],
    ids=[
        "one",
        "backwards",
    ],
)
def test_rearrange_indexes(current, instruction, expected):
    ll = Msg(current)
    ret = rearrange(ll, instruction)
    assert str(ret) == str(expected)


def test_msg():
    ll = Msg([4, 5, 6])
    assert str(ll) == "4, 5, 6"


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = None
    ret = parse(example_data)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 3
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
