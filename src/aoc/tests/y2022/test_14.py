#!/usr/bin/env python
"""Tests for AoC 14, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d14 import Cave, parse, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=14)
    return puzzle.example_data


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = [
        (0, 9),
        (1, 9),
        (2, 6),
        (2, 9),
        (3, 6),
        (3, 9),
        (4, 4),
        (4, 5),
        (4, 6),
        (4, 9),
        (5, 9),
        (6, 9),
        (7, 9),
        (8, 4),
        (8, 5),
        (8, 6),
        (8, 7),
        (8, 8),
        (8, 9),
        (9, 4),
    ]
    assert sorted(parse(example_data).walls) == sorted(expected)


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 24
    ret = solve_part_one(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 93
    ret = solve_part_two(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


@pytest.mark.parametrize(
    "path_string, expected",
    [
        ("498,4 -> 498,6 -> 496,6", [(498, 4), (498, 5), (498, 6), (496, 6), (497, 6)]),
        (
            "503,4 -> 502,4 -> 502,9 -> 494,9",
            [
                (503, 4),
                (502, 4),
                (502, 5),
                (502, 6),
                (502, 7),
                (502, 8),
                (502, 9),
                (501, 9),
                (500, 9),
                (499, 9),
                (498, 9),
                (497, 9),
                (496, 9),
                (495, 9),
                (494, 9),
            ],
        ),
    ],
)
def test_parse_path(path_string, expected):
    assert sorted(list(Cave.parse_path(path_string))) == sorted(expected)
