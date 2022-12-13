#!/usr/bin/env python
"""Tests for AoC 12, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d12 import parse, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=12)
    return puzzle.example_data


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example_data):
    """Test that input is parsed properly"""
    expected = None
    assert parse(example_data) == expected


def test_part1_example1(example_data):
    """Test part 1 on example input"""
    expected = 31
    assert solve_part_one(parse(example_data)) == expected


def test_part2():
    input_data = """Sabqponm
abcryxxl
accszExk
ccctuvwj
acdefghi"""
    hill = parse(input_data)
    print(hill.neighbors((7, 0)))
    expected = 30
    assert solve_part_two(hill) == expected


def test_part2_example2(example_data):
    """Test part 2 on example input"""
    # expected = 29
    expected = 29
    assert solve_part_two(parse(example_data)) == expected
