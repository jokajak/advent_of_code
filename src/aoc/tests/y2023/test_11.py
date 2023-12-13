#!/usr/bin/env python
"""Tests for AoC 11, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d11 import parse, solve_part_one, solve_part_two, expand_graph


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=11)
    return puzzle.examples[0].input_data


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = None
    ret = parse(example_data)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 374
    ret = solve_part_one(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


@pytest.mark.parametrize(
    "expansion_rate, expected",
    [
        (5, 7),
        (10, 1030),
        (100, 8410),
    ],
)
def test_part2(example_data, expansion_rate, expected):
    """Test part 2 on example input"""
    ret = solve_part_two(parse(example_data), expansion_rate=expansion_rate)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


@pytest.mark.parametrize(
    "input_graph, expansion_rate, expected",
    [
        ({0: {0: "#", 1: "#"}}, 1, {0: {0: "#", 1: "#"}}),
        ({0: {0: "#", 2: "#"}}, 1, {0: {0: "#", 3: "#"}}),
        ({0: {0: "#", 1: "#"}}, 2, {0: {0: "#", 1: "#"}}),
        ({0: {0: "#", 2: "#"}}, 2, {0: {0: "#", 4: "#"}}),
        ({0: {0: "#", 2: "#"}}, 5, {0: {0: "#", 7: "#"}}),
        ({0: {0: "#", 3: "#"}}, 5, {0: {0: "#", 13: "#"}}),
        ({0: {0: "#", 2: "#", 4: "#"}}, 5, {0: {0: "#", 7: "#", 14: "#"}}),
        ({0: {0: "#"}, 1: {0: "#"}}, 1, {0: {0: "#"}, 1: {0: "#"}}),
        ({0: {0: "#"}, 2: {0: "#"}}, 1, {0: {0: "#"}, 3: {0: "#"}}),
        ({0: {0: "#"}, 2: {0: "#"}}, 2, {0: {0: "#"}, 4: {0: "#"}}),
        ({0: {0: "#"}, 2: {0: "#"}}, 5, {0: {0: "#"}, 7: {0: "#"}}),
        ({0: {0: "#"}, 3: {0: "#"}}, 5, {0: {0: "#"}, 13: {0: "#"}}),
        (
            {0: {0: "#"}, 2: {0: "#"}, 4: {0: "#"}},
            5,
            {0: {0: "#"}, 7: {0: "#"}, 14: {0: "#"}},
        ),
        (
            {
                0: {0: "#"},
                1: {0: "#"},
                2: {0: "#"},
                4: {0: "#"},
                5: {0: "#"},
                6: {0: "#"},
            },
            10,
            {0: {0: "#"}, 1: {0: "#"}, 2: {0: "#"}, 14: {0: "#"}, 15: {0: "#"}},
        ),
    ],
)
def test_expand_graph(input_graph, expansion_rate, expected):
    ret = expand_graph(input_graph, expansion_rate)
    assert ret == expected
