#!/usr/bin/env python
"""Tests for AoC 10, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d10 import (
    get_signal_strength,
    parse,
    run_program,
    solve_part_one,
    solve_part_two,
)


@pytest.fixture
def example_data():
    example_data = """addx 15
    addx -11
    addx 6
    addx -3
    addx 5
    addx -1
    addx -8
    addx 13
    addx 4
    noop
    addx -1
    addx 5
    addx -1
    addx 5
    addx -1
    addx 5
    addx -1
    addx 5
    addx -1
    addx -35
    addx 1
    addx 24
    addx -19
    addx 1
    addx 16
    addx -11
    noop
    noop
    addx 21
    addx -15
    noop
    noop
    addx -3
    addx 9
    addx 1
    addx -3
    addx 8
    addx 1
    addx 5
    noop
    noop
    noop
    noop
    noop
    addx -36
    noop
    addx 1
    addx 7
    noop
    noop
    noop
    addx 2
    addx 6
    noop
    noop
    noop
    noop
    noop
    addx 1
    noop
    noop
    addx 7
    addx 1
    noop
    addx -13
    addx 13
    addx 7
    noop
    addx 1
    addx -33
    noop
    noop
    noop
    addx 2
    noop
    noop
    noop
    addx 8
    noop
    addx -1
    addx 2
    addx 1
    noop
    addx 17
    addx -9
    addx 1
    addx 1
    addx -3
    addx 11
    noop
    noop
    addx 1
    noop
    addx 1
    noop
    noop
    addx -13
    addx -19
    addx 1
    addx 3
    addx 26
    addx -30
    addx 12
    addx -1
    addx 3
    addx 1
    noop
    noop
    noop
    addx -9
    addx 18
    addx 1
    addx 2
    noop
    noop
    addx 9
    noop
    noop
    noop
    addx -1
    addx 2
    addx -37
    addx 1
    addx 3
    noop
    addx 15
    addx -21
    addx 22
    addx -6
    addx 1
    noop
    addx 2
    addx 1
    noop
    addx -10
    noop
    noop
    addx 20
    addx 1
    addx 2
    addx 2
    addx -6
    addx -11
    noop
    noop
    noop"""
    return example_data


def test_parse_example1():
    """Test that input is parsed properly"""
    example_data = """noop
addx 3
addx -5"""
    # Before first cycle: 1
    # First instruction: noop
    # After first cycle: 1
    # Before second cyle: 1
    # Second instruction: addx 3
    # After second cycle: 1
    # Before third cycle: 1
    # Third instruction: addx -5
    # After third cycle: 1
    # Before fourth cycle: 4
    # After fourth cycle: 4
    # j
    # 3: 1 addx 3
    # noop
    # noop

    expected = {1: 0, 3: 3, 5: -5, "last_instruction": 5}
    assert parse(example_data) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            """noop
addx 3
addx -5
noop""",
            -1,
        ),
        (
            """addx 15
    addx -11
    addx 6
    addx -3
    addx 5
    addx -1
    addx -8
    addx 13
    addx 4
    noop""",
            21,
        ),
    ],
)
def test_run_program(test_input, expected):
    assert run_program(parse(test_input)) == expected


def test_run_program_short():
    test_input = """addx 15
    addx -11
    addx 6
    addx -3
    addx 5
    addx -1
    addx -8
    addx 13
    addx 4
    noop
    addx -1"""
    expected = 21
    assert run_program(parse(test_input), 20) == expected


def test_get_signal_strength(example_data):
    assert get_signal_strength(parse(example_data), 20) == 420
    assert get_signal_strength(parse(example_data), 60) == 1140
    assert get_signal_strength(parse(example_data), 100) == 1800
    assert get_signal_strength(parse(example_data), 140) == 2940
    assert get_signal_strength(parse(example_data), 180) == 2880
    assert get_signal_strength(parse(example_data), 220) == 3960


def test_part1_example1(example_data):
    """Test part 1 on example input"""
    expected = 13140
    assert solve_part_one(parse(example_data)) == expected


@pytest.mark.parametrize(
    "cycle, expected",
    [
        (1, 1),
        (2, 1),
        (3, 16),
        (4, 16),
        (5, 5),
        (6, 5),
        (7, 11),
        (8, 11),
    ],
)
def test_part2_runs(example_data, cycle, expected):
    assert run_program(parse(example_data), cycle) == expected


def test_part2_example2(example_data):
    """Test part 2 on example input"""
    expected = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""
    assert solve_part_two(parse(example_data)) == expected
