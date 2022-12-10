#!/usr/bin/env python
"""Tests for AoC 9, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d09 import (
    calculate_tail_position,
    calculate_visited_positions,
    parse,
    solve_part_one,
    solve_part_two,
)


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=9)
    example_data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
    return example_data


@pytest.mark.parametrize(
    "head_position, tail_position, expected",
    [
        ((0, 0), (0, 0), (0, 0)),
        ((1, 0), (0, 0), (0, 0)),
        ((2, 0), (0, 0), (1, 0)),
        ((1, 2), (0, 0), (1, 1)),
        ((1, -2), (0, 0), (1, -1)),
        ((-1, -1), (0, 0), (0, 0)),
    ],
)
def test_calculate_tail_position(head_position, tail_position, expected):
    """Test calculate tail position"""
    assert calculate_tail_position(head_position, tail_position) == expected


@pytest.mark.parametrize(
    "start_position, movements, expected",
    [
        ((0, 0), [("R", 4)], {(0, 0): 1, (1, 0): 1, (2, 0): 1, (3, 0): 1}),
        (
            (0, 0),
            [("R", 4), ("U", 4)],
            {
                (0, 0): 1,
                (1, 0): 1,
                (2, 0): 1,
                (3, 0): 1,
                (4, 1): 1,
                (4, 2): 1,
                (4, 3): 1,
            },
        ),
        (
            (0, 0),
            [("R", 4), ("U", 4), ("L", 3)],
            {
                (0, 0): 1,
                (1, 0): 1,
                (2, 0): 1,
                (3, 0): 1,
                (4, 1): 1,
                (4, 2): 1,
                (4, 3): 1,
                (3, 4): 1,
                (2, 4): 1,
            },
        ),
        (
            (0, 0),
            [("R", 4), ("U", 4), ("L", 3), ("D", 1)],
            {
                (0, 0): 1,
                (1, 0): 1,
                (2, 0): 1,
                (3, 0): 1,
                (4, 1): 1,
                (4, 2): 1,
                (4, 3): 1,
                (3, 4): 1,
                (2, 4): 1,
            },
        ),
        (
            (0, 0),
            [("R", 4), ("U", 4), ("L", 3), ("D", 1), ("R", 4)],
            {
                (0, 0): 1,
                (1, 0): 1,
                (2, 0): 1,
                (3, 0): 1,
                (4, 1): 1,
                (4, 2): 1,
                (4, 3): 2,
                (3, 4): 1,
                (2, 4): 1,
                (3, 3): 1,
            },
        ),
    ],
)
def test_calculate_visited_positions(start_position, movements, expected):
    """Test calculate visited positions"""
    assert calculate_visited_positions(start_position, movements) == expected


def test_parse_example1(example_data):
    """Test that input is parsed properly"""
    expected = [
        ("R", 4),
        ("U", 4),
        ("L", 3),
        ("D", 1),
        ("R", 4),
        ("D", 1),
        ("L", 5),
        ("R", 2),
    ]
    assert parse(example_data) == expected


def test_part1_example1(example_data):
    """Test part 1 on example input"""
    expected = 13
    assert solve_part_one(parse(example_data)) == expected


def test_part2_example2():
    """Test part 2 on example input"""
    expected = 36
    input_data = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
    assert solve_part_two(parse(input_data)) == expected
