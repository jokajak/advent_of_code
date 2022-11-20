#!/usr/bin/env python
"""Tests for AoC 1, 2021"""

# Third party imports
from aocd.models import Puzzle
from aoc.2021.1 import parse, solve_part_one, solve_part_two
import pytest

@pytest.fixture
def example1():
    puzzle = Puzzle(year=2021, day=1)
    return puzzle.example_data

@pytest.fixture
def example2():
    return parse(puzzle_input)

@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 == None

def test_part1_example1(example1):
    """Test part 1 on example input"""
    expected = None
    assert solve_part_one(example1) == expected

def test_part2_example2(example2):
    """Test part 2 on example input"""
    expected = None
    assert solve_part_two(example2) == expected