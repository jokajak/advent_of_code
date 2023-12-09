#!/usr/bin/env python
"""Tests for AoC 5, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d05 import (
    parse,
    solve_part_one,
    solve_part_two,
    parse_map,
    get_map_range,
)


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=5)
    return puzzle.examples[0].input_data


def test_parse_map():
    expected = None
    input_data = ["50 98 2", "52 50 48"]
    if expected is None:
        pytest.skip("Not yet implemented")
    ret = parse_map(input_data)
    assert ret == expected


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = None
    ret = parse(example_data)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 35
    ret = solve_part_one(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 46
    ret = solve_part_two(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


@pytest.mark.parametrize(
    "input_range, map_values, expected",
    [
        (
            (79, 93),
            (52, 50, 48),
            [(81, 95)],
        ),
        (
            (11, 20),
            (1, 5, 10),
            [(7, 15), (16, 20)],
        ),
        (
            (11, 20),
            (1, 5, 2),
            [(11, 20)],
        ),
    ],
)
def test_get_map_range(input_range, map_values, expected):
    ret = get_map_range(input_range, map_values)
    assert ret == expected
