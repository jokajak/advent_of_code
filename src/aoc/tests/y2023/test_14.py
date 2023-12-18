#!/usr/bin/env python
"""Tests for AoC 14, 2023"""

import pytest

# Third party imports
from aocd.models import Puzzle
from aoc.y2023.d14 import (
    hash_graph,
    parse,
    print_graph,
    solve_part_one,
    solve_part_two,
    run_cycle,
    tilt_graph,
)


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2023, day=14)
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
    expected = 136
    ret = solve_part_one(parse(example_data))
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected


def test_cycles(example_data):
    expected = """.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#...."""
    print(expected)
    expected = "".join(expected.splitlines())
    graph = parse(example_data)
    print_graph(graph)
    graph = tilt_graph(graph, delta_x=0, delta_y=-1)
    print_graph(graph)
    graph = tilt_graph(graph, delta_x=-1, delta_y=0)
    print_graph(graph)
    graph = tilt_graph(graph, delta_x=0, delta_y=1)
    print_graph(graph)
    graph = tilt_graph(graph, delta_x=1, delta_y=0)
    print_graph(graph)
    assert hash_graph(graph.graph) == expected


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 64
    ret = solve_part_two(parse(example_data), cycles=20)
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected
