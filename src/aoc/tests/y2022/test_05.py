#!/usr/bin/env python
"""Tests for AoC 5, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d05 import (
    parse,
    parse_initialization,
    process_instruction,
    solve_part_one,
    solve_part_two,
)


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=5)
    return puzzle.example_data


def test_parse_initial_data():
    """Test that my input is parsed."""
    expected = [
        [
            "H",
            "T",
            "Z",
            "D",
        ],
        ["Q", "R", "W", "T", "G", "C", "S"],
        ["P", "B", "F", "Q", "N", "R", "C", "H"],
        ["L", "C", "N", "F", "H", "Z"],
        ["G", "L", "F", "Q", "S"],
        ["V", "P", "W", "Z", "B", "R", "C", "S"],
        ["Z", "F", "J"],
        ["D", "L", "V", "Z", "R", "H", "Q"],
        ["B", "H", "G", "N", "F", "Z", "L", "D"],
    ]
    puzzle = Puzzle(year=2022, day=5)
    input_data = puzzle.input_data
    assert parse_initialization(input_data) == expected


def test_parse_example1(example_data):
    """Test that input is parsed properly"""
    expected = [
        ["Z", "N"],
        ["M", "C", "D"],
        ["P"],
    ]
    initialization_data, steps = parse(example_data)
    assert initialization_data == expected


def test_process_instruction():
    state = [
        ["Z", "N"],
        ["M", "C", "D"],
        ["P"],
    ]
    instruction = (1, 2, 1)
    res = process_instruction(state, instruction)
    expected = [
        ["Z", "N", "D"],
        [
            "M",
            "C",
        ],
        ["P"],
    ]
    assert res == expected


def test_part1_example1(example_data):
    """Test part 1 on example input"""
    expected = "CMZ"
    assert solve_part_one(parse(example_data)) == expected


def test_part2_example2(example_data):
    """Test part 2 on example input"""
    expected = "MCD"
    assert solve_part_two(parse(example_data)) == expected
