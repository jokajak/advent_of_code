#!/usr/bin/env python
"""Tests for AoC 3, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d03 import (
    parse,
    solve_part_one,
    solve_part_two,
    get_number,
    find_numbers_around_symbol,
)


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=3)
    return puzzle.examples[0].input_data


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected_string = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
    # fmt: off
    expected = {
    (0, 0): 4, (0, 1): 6, (0, 2): 7, (0, 3): '.', (0, 4): '.', (0, 5): 1, (0, 6): 1, (0, 7): 4, (0, 8): '.', (0, 9): '.',
    (1, 0): '.', (1, 1): '.', (1, 2): '.', (1, 3): '*', (1, 4): '.', (1, 5): '.', (1, 6): '.', (1, 7): '.', (1, 8): '.', (1, 9): '.',
    (2, 0): '.', (2, 1): '.', (2, 2): 3, (2, 3): 5, (2, 4): '.', (2, 5): '.', (2, 6): 6, (2, 7): 3, (2, 8): 3, (2, 9): '.',
    (3, 0): '.', (3, 1): '.', (3, 2): '.', (3, 3): '.', (3, 4): '.', (3, 5): '.', (3, 6): '#', (3, 7): '.', (3, 8): '.', (3, 9): '.',
    (4, 0): 6, (4, 1): 1, (4, 2): 7, (4, 3): '*', (4, 4): '.', (4, 5): '.', (4, 6): '.', (4, 7): '.', (4, 8): '.', (4, 9): '.',
    (5, 0): '.', (5, 1): '.', (5, 2): '.', (5, 3): '.', (5, 4): '.', (5, 5): '+', (5, 6): '.', (5, 7): 5, (5, 8): 8, (5, 9): '.',
    (6, 0): '.', (6, 1): '.', (6, 2): 5, (6, 3): 9, (6, 4): 2, (6, 5): '.', (6, 6): '.', (6, 7): '.', (6, 8): '.', (6, 9): '.',
    (7, 0): '.', (7, 1): '.', (7, 2): '.', (7, 3): '.', (7, 4): '.', (7, 5): '.', (7, 6): 7, (7, 7): 5, (7, 8): 5, (7, 9): '.',
    (8, 0): '.', (8, 1): '.', (8, 2): '.', (8, 3): '$', (8, 4): '.', (8, 5): '*', (8, 6): '.', (8, 7): '.', (8, 8): '.', (8, 9): '.',
    (9, 0): '.', (9, 1): 6, (9, 2): 6, (9, 3): 4, (9, 4): '.', (9, 5): 5, (9, 6): 9, (9, 7): 8, (9, 8): '.', (9, 9): '.',
}
    # fmt: on

    parsed = parse(example_data)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert parsed == expected


def test_get_number(example_data):
    grid = parse(example_data)
    expected_coord, expected_val = (0, 0), 467
    coord, value = get_number(grid, (0, 2))
    assert coord == expected_coord
    assert value == expected_val
    expected_coord, expected_val = (4, 0), 617
    coord, value = get_number(grid, (4, 2))
    assert coord == expected_coord
    assert value == expected_val
    expected_coord, expected_val = (2, 2), 35
    coord, value = get_number(grid, (2, 3))
    assert coord == expected_coord
    assert value == expected_val
    expected_coord, expected_val = (2, 2), 35
    coord, value = get_number(grid, (2, 2))
    assert coord == expected_coord
    assert value == expected_val


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 4361
    ret = solve_part_one(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 467835
    ret = solve_part_two(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected
