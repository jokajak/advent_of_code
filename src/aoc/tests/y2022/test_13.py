#!/usr/bin/env python
"""Tests for AoC 13, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d13 import is_ordered, parse, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=13)
    return puzzle.example_data


@pytest.mark.parametrize(
    "left, right, expected",
    [
        ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1], True),
        ([[1], [2, 3, 4]], [[1], 4], True),
        ([[4, 4], 4, 4], [[4, 4], 4, 4, 4], True),
        ([9], [[8, 7, 6]], False),
        ([[8], 8], [[], 6, [0, 8, 8], []], False),
        ([0, 0, 0], [[2]], True),
        ([0], [2, 0, 0], True),
    ],
)
def test_is_ordered(left, right, expected):
    assert is_ordered(left, right) == expected


def test_parse_example1(example_data):
    """Test that input is parsed properly"""
    expected = [
        ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]),
        ([[1], [2, 3, 4]], [[1], 4]),
        ([9], [[8, 7, 6]]),
        ([[4, 4], 4, 4], [[4, 4], 4, 4, 4]),
        ([7, 7, 7, 7], [7, 7, 7]),
        ([], [3]),
        ([[[]]], [[]]),
        ([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]),
    ]
    assert parse(example_data) == expected


def test_part1_example1(example_data):
    """Test part 1 on example input"""
    expected = 13
    assert solve_part_one(parse(example_data)) == expected


def test_part2_example2(example_data):
    """Test part 2 on example input"""
    expected = 140
    assert solve_part_two(parse(example_data)) == expected
