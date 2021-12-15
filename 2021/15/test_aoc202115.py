"""Tests for AoC 15, 2021"""

# Standard library imports
import pathlib

# Third party imports
import aoc202115
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202115.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202115.parse(puzzle_input)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 == ...


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc202115.part1(example1) == 40


def test_part2_example2(example1):
    """Test part 2 map is generated properly."""
    assert aoc202115.expand_map(example1) == example2

def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc202115.part2(example2) == 315
