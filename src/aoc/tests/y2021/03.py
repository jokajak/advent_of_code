#!/usr/bin/env python
"""Tests for AoC 3, 2021"""

# Third party imports
from aocd.models import Puzzle
from aoc.y2021.d03 import parse, solve_part_one, solve_part_two
import pytest


@pytest.fixture
def example1():
    puzzle = Puzzle(year=2021, day=3)
    return puzzle.example_data.splitlines()


@pytest.fixture
def example2():
    puzzle = Puzzle(year=2021, day=3)
    return puzzle.example_data.splitlines()


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 is None


def test_part1_example1(example1):
    """Test part 1 on example input"""
    expected = 198
    assert solve_part_one(example1) == expected


def test_part2_example2(example2):
    """Test part 2 on example input"""
    expected = 230
    assert solve_part_two(example2) == expected
