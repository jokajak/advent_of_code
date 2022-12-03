#!/usr/bin/env python
"""Tests for AoC 1, 2022"""

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d01 import parse, solve_part_one, solve_part_two
import pytest


@pytest.fixture
def example1():
    puzzle = Puzzle(year=2022, day=1)
    return parse(puzzle.example_data)


@pytest.fixture
def example2():
    puzzle = Puzzle(year=2022, day=1)
    puzzle_input = puzzle.example_data
    return parse(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly"""
    expected = [
        "1000",
        "2000",
        "3000",
        "",
        "4000",
        "",
        "5000",
        "6000",
        "",
        "7000",
        "8000",
        "9000",
        "",
        "10000",
    ]
    assert example1 == expected


def test_part1_example1(example1):
    """Test part 1 on example input"""
    expected = 24000
    assert solve_part_one(example1) == expected


def test_part2_example2(example2):
    """Test part 2 on example input"""
    print(example2)
    expected = 45000
    assert solve_part_two(example2) == expected
