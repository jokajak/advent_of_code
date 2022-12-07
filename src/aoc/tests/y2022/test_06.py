#!/usr/bin/env python
"""Tests for AoC 6, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.communications import Message
from aoc.y2022.d06 import parse, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=6)
    return puzzle.example_data


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example_data):
    """Test that input is parsed properly"""
    expected = example_data
    assert parse(example_data) == expected


def test_part1_example1(example_data):
    """Test part 1 on example input"""
    expected = 7
    assert solve_part_one(parse(example_data)) == expected


def test_part2_example2(example_data):
    """Test part 2 on example input"""
    expected = 19
    assert solve_part_two(parse(example_data)) == expected
