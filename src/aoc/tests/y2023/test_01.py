#!/usr/bin/env python
"""Tests for AoC 1, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d01 import (
    parse,
    solve_part_one,
    solve_part_two,
    find_first_number,
    find_last_number,
)


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=1)
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
    expected = None
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


def test_find_first_number():
    assert find_first_number("eightwone") == "eight"


def test_find_last_number():
    assert find_last_number("eightwone") == "one"
