#!/usr/bin/env python
"""Tests for AoC 9, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d09 import (
    parse,
    solve_part_one,
    solve_part_two,
    next_arithmetic_sequence_value,
    get_differences,
    get_next_value,
)


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=9)
    return puzzle.examples[0].input_data


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = [
        [0, 3, 6, 9, 12, 15],
        [1, 3, 6, 10, 15, 21],
        [10, 13, 16, 21, 30, 45],
    ]
    ret = parse(example_data)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ((0, 3, 6, 9), 12),
        ((3, 6, 9), 12),
    ],
)
def test_get_next_arithmetic_value(input_data, expected):
    ret = next_arithmetic_sequence_value(input_data)
    assert ret == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ((0, 3, 6, 9), [3, 3, 3]),
        ((3, 6, 9), [3, 3]),
        ((1, 3, 6, 10, 15, 21), [2, 3, 4, 5, 6]),
    ],
)
def test_get_differences(input_data, expected):
    ret = get_differences(input_data)
    assert ret == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ((0, 3, 6, 9), 12),
        ((3, 6, 9), 12),
        ((1, 3, 6, 10, 15, 21), 28),
        ((10, 13, 16, 21, 30, 45), 68),
    ],
)
def test_get_next_value(input_data, expected):
    ret = get_next_value(input_data)
    assert ret == expected


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 114
    ret = solve_part_one(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 2
    ret = solve_part_two(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected
