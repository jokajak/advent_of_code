"""Tests for AoC 12, 2021"""

# Standard library imports
import pathlib

# Third party imports
import aoc202112
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202112.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202112.parse(puzzle_input)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 == ...


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc202112.part1(example1) == 10


def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc202112.part2(example2) == 36
