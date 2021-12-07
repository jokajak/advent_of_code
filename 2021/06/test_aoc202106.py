"""Tests for AoC 6, 2021"""

# Standard library imports
import pathlib

# Third party imports
import aoc202106
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202106.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202106.parse(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 == [3, 4, 3, 1, 2]


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc202106.part1(example1, 18) == 26
    assert aoc202106.part1(example1, 80) == 5934


def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc202106.part2(example2) == 26984457539
