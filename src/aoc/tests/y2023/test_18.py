#!/usr/bin/env python
"""Tests for AoC 18, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d18 import parse, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=18)
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
    expected = 62
    ret = solve_part_one(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 952408144115
    ret = solve_part_two(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected