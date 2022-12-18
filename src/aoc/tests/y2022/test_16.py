#!/usr/bin/env python
"""Tests for AoC 16, 2022"""

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.d16 import calculate_distances, parse, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=16)
    return puzzle.example_data


def test_parse(example_data):
    """Test that input is parsed properly"""
    expected = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
    """
    volcano = parse(example_data)
    assert "\n".join(str(v) for _, v in volcano.nodes.items()) == expected


def test_distances(example_data):
    graph = parse(example_data)
    assert calculate_distances(graph) == graph.calculate_distances()


def test_part1(example_data):
    """Test part 1 on example input"""
    expected = 1651
    input_data = parse(example_data)
    ret = solve_part_one(input_data)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 1707
    ret = solve_part_two(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected
