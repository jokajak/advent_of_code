#!/usr/bin/env python
"""Tests for AoC 6, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d06 import parse, solve_part_one, solve_part_two, calculate_distance


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=6)
    return puzzle.examples[0].input_data


@pytest.mark.parametrize(
    "total_time, acceleration_time, expected_value",
    [
        (7, 0, 0),
        (7, 1, 6),
        (7, 2, 10),
        (7, 3, 12),
        (7, 4, 12),
        (7, 5, 10),
        (7, 6, 6),
        (7, 7, 0),
    ],
)
def test_calculate_distance(total_time, acceleration_time, expected_value):
    distance = calculate_distance(total_time, acceleration_time)
    assert distance == expected_value


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = ([7, 15, 30], [9, 40, 200])
    ret = parse(example_data)
    times, distances = ret
    times = list(times)
    distances = list(distances)
    ret = (times, distances)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 288
    ret = solve_part_one(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 71503
    ret = solve_part_two(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected
