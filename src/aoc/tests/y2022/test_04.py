#!/usr/bin/env python
"""Tests for AoC 4, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d04 import parse, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=4)
    return puzzle.example_data


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example_data):
    """Test that input is parsed properly"""
    expected = [
        "2-4,6-8",
        "2-3,4-5",
        "5-7,7-9",
        "2-8,3-7",
        "6-6,4-6",
        "2-6,4-8",
    ]
    assert parse(example_data) == expected


def test_part1_example1(example_data):
    """Test part 1 on example input"""
    expected = 2
    assert solve_part_one(parse(example_data)) == expected


def test_part2_example2(example_data):
    """Test part 2 on example input"""
    expected = 4
    assert solve_part_two(parse(example_data)) == expected
