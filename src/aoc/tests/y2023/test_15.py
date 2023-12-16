#!/usr/bin/env python
"""Tests for AoC 15, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d15 import parse, solve_part_one, solve_part_two, hash_string


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=15)
    return puzzle.examples[0].input_data


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("HASH", 52),
        ("rn=1", 30),
    ],
)
def test_hash_string(input_string, expected):
    assert hash_string(input_string) == expected


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = None
    ret = parse(example_data)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 1320
    ret = solve_part_one(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 145
    ret = solve_part_two(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected
