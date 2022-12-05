#!/usr/bin/env python
"""Tests for AoC 5, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d05 import parse, process_instruction, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=5)
    return puzzle.example_data


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
