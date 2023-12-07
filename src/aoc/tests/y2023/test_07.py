#!/usr/bin/env python
"""Tests for AoC 7, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d07 import (
    parse,
    solve_part_one,
    solve_part_two,
    sort_hands_part_1,
    get_hand_type,
    rank_hands,
    sort_hands,
)


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=7)
    return puzzle.examples[0].input_data


@pytest.mark.parametrize(
    "left_hand, right_hand, expected",
    [
        ("A", "A", 0),
        ("A", "K", 1),
        ("KK677", "KTJJT", 1),
        ("QQQJA", "T55J5", 1),
        ("QJJJJ", "KJJJJ", -1),
    ],
)
def test_sort_hands_part_1(left_hand, right_hand, expected):
    ret = sort_hands_part_1(left_hand, right_hand)
    assert ret == expected or ret > 0 and expected > 0 or ret < 0 and expected < 0


@pytest.mark.parametrize(
    "hand, jokers_wild, expected",
    [
        ("32T3K", False, 1),
        ("KTJJT", False, 2),
    ],
)
def test_get_hand_type(hand, jokers_wild, expected):
    ret = get_hand_type(hand)
    assert ret == expected


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = {"32T3K": 765, "T55J5": 684, "KK677": 28, "KTJJT": 220, "QQQJA": 483}

    ret = parse(example_data)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 6440
    ret = solve_part_one(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


@pytest.mark.parametrize(
    "hands, expected",
    [
        (
            ["32T3K", "T55J5", "KK677", "KTJJT", "QQQJA"],
            ["32T3K", "KK677", "T55J5", "QQQJA", "KTJJT"],
        ),
        (["AAQAA", "AAJ4A"], ["AAJ4A", "AAQAA"]),
    ],
)
def test_sort_hands(hands, expected):
    ret = sort_hands(hands)
    assert ret == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 5905
    ret = solve_part_two(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected
