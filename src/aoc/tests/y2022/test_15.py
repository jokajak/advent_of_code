#!/usr/bin/env python
"""Tests for AoC 15, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d15 import parse, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=15)
    return puzzle.example_data


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = None
    assert parse(example_data) == expected


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 26
    ret = solve_part_one(parse(example_data), y=10)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 56000011
    ret = solve_part_two(parse(example_data), search_area=20)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected
