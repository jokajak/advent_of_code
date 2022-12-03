#!/usr/bin/env python
"""Tests for AoC 2, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d02 import parse, score_round, solve_part_one, solve_part_two


@pytest.fixture
def example1():
    puzzle = Puzzle(year=2022, day=2)
    return puzzle.example_data


@pytest.fixture
def example2():
    puzzle = Puzzle(year=2022, day=2)
    return parse(puzzle.example_data)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 is None


def test_score_round():
    """Test scoring a round."""
    expected = 8
    assert score_round("A", "Y") == expected


def test_part1_example1(example1):
    """Test part 1 on example input"""
    expected = 15
    assert solve_part_one(parse(example1)) == expected


def test_part2_example2(example2):
    """Test part 2 on example input"""
    expected = 12
    assert solve_part_two(example2) == expected
