"""Tests for AoC 10, 2021"""

# Standard library imports
import pathlib

# Third party imports
import aoc202110
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202110.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202110.parse(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 == []


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc202110.part1(example1) == 26397


def test_closing_score():
    assert aoc202110.SyntaxValidator.score_closing_brackets("}}]])})]") == 288957


def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc202110.part2(example2) == 288957
