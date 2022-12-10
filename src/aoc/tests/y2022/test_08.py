#!/usr/bin/env python
"""Tests for AoC 8, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d08 import (
    expand_grid,
    parse,
    position_is_visible,
    scenic_score,
    solve_part_one,
    solve_part_two,
)


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=8)
    return puzzle.example_data


def test_expand_grid():
    """Test the grid expands"""
    expected = [[-1, -1, -1], [-1, 1, -1], [-1, -1, -1]]
    assert expand_grid([[1]]) == expected


def test_position_is_visible():
    """Test that visibility testing works"""
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    assert position_is_visible(grid, 1, 1) is True

    grid = expand_grid(
        [
            [3, 0, 3, 7, 3],
            [2, 5, 5, 1, 2],
            [6, 5, 3, 3, 2],
            [3, 3, 5, 4, 9],
            [3, 5, 3, 9, 0],
        ]
    )
    assert position_is_visible(grid, 1, 1) is True
    assert position_is_visible(grid, 2, 4) is False
    assert position_is_visible(grid, 3, 3) is False
    assert position_is_visible(grid, 3, 4) is True
    assert position_is_visible(grid, 4, 3) is True


def test_parse_example1(example_data):
    """Test that input is parsed properly"""
    expected = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]
    assert parse(example_data) == expected


def test_part1_example1(example_data):
    """Test part 1 on example input"""
    expected = 21
    assert solve_part_one(parse(example_data)) == expected


def test_scenic_score(example_data):
    """Test calculating the scenic score"""
    expected = 4
    assert scenic_score(expand_grid(parse(example_data)), 2, 3) == expected
    assert scenic_score(expand_grid(parse(example_data)), 4, 3) == 8


def test_part2_example2(example_data):
    """Test part 2 on example input"""
    expected = 8
    assert solve_part_two(parse(example_data)) == expected
