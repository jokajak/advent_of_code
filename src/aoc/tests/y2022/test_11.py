#!/usr/bin/env python
"""Tests for AoC 11, 2022"""

import operator

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d11 import Monkey, parse, run_rounds, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=11)
    return puzzle.example_data


def test_monkey_line_parse():
    """Test parsing lines"""
    expected = Monkey(operator.mul, 19, 23, 2, 3)
    input_data = """
        Starting items: 79, 98
        Operation: new = old * 19
        Test: divisible by 23
          If true: throw to monkey 2
          If false: throw to monkey 3
    """
    ret = Monkey.read_lines(input_data.splitlines())
    assert ret == expected


@pytest.mark.parametrize(
    "rounds, expected",
    [
        (
            1,
            """Monkey 0: 20, 23, 27, 26
Monkey 1: 2080, 25, 167, 207, 401, 1046
Monkey 2:
Monkey 3:""",
        ),
        (
            2,
            """Monkey 0: 695, 10, 71, 135, 350
Monkey 1: 43, 49, 58, 55, 362
Monkey 2:
Monkey 3:""",
        ),
        (
            20,
            """Monkey 0: 10, 12, 14, 26, 34
Monkey 1: 245, 93, 53, 199, 115
Monkey 2:
Monkey 3:""",
        ),
    ],
)
def test_run_round(example_data, rounds, expected):
    # print(example_data)
    monkeys = parse(example_data)
    print(f"After round {rounds}")
    print(str_round(monkeys))
    monkeys = run_rounds(monkeys, rounds)
    ret = str_round(monkeys)
    assert ret == expected


def str_round(monkeys):
    ret = []
    for i, monkey in enumerate(monkeys):
        ret.append(f"Monkey {i}: {monkey.monkey_items()}".strip())
    return "\n".join(ret)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example_data):
    """Test that input is parsed properly"""
    expected = None
    assert parse(example_data) == expected


def test_part1_example1(example_data):
    """Test part 1 on example input"""
    expected = 10605
    assert solve_part_one(parse(example_data)) == expected


def test_part2_run(example_data):
    """Test part2 runs"""
    monkeys = run_rounds(parse(example_data, nervous=False), 1)
    print(str_round(monkeys))
    ret = [monkey.total_items_touched for monkey in monkeys]
    expected = [2, 4, 3, 6]
    assert ret == expected


def test_part2_example2(example_data):
    """Test part 2 on example input"""
    expected = 2713310158
    assert solve_part_two(parse(example_data, nervous=False)) == expected
