#!/usr/bin/env python
"""Tests for AoC 2, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d02 import parse, solve_part_one, solve_part_two, parse_game


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=2)
    return puzzle.examples[0].input_data


def test_parse_game():
    expected_id, expected_result = (
        1,
        [{"blue": 3, "red": 4}, {"red": 1, "green": 2, "blue": 6}, {"green": 2}],
    )
    id, parsed_game = parse_game(
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    )
    assert expected_id == id
    assert expected_result == parsed_game


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = None
    ret = parse(example_data)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 8
    ret = solve_part_one(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 2286
    ret = solve_part_two(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected
