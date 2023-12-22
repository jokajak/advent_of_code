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
    expected_graph = parse(expected)
    graph = parse(example_data)
    graph = tilt_graph(graph, delta_x=0, delta_y=-1)
    graph = tilt_graph(graph, delta_x=-1, delta_y=0)
    graph = tilt_graph(graph, delta_x=0, delta_y=1)
    graph = tilt_graph(graph, delta_x=1, delta_y=0)
    print("Final graph then expected")
    print(hash_graph(graph))
    print(hash_graph(expected_graph))
    print(hash_graph(graph.graph))
    print(hash_graph(expected_graph.graph))
    print_graph(graph)
    print_graph(expected_graph)
    assert hash_graph(graph) == hash_graph(expected_graph)


def test_cycle(example_data):
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
    graph = parse(example_data)
    graph = run_cycle(graph)
    assert hash_graph(graph) == hash_graph(parse(expected))
    graph = run_cycle(graph)
    expected_2 = """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O"""
    assert hash_graph(graph) == hash_graph(parse(expected_2))
    graph = run_cycle(graph)
    expected_3 = """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O"""
    print("cycle 3")
    print_graph(graph)
    print("expected")
    print_graph(parse(expected_3))
    assert hash_graph(graph) == hash_graph(parse(expected_3))


def test_part2(example_data):
    """Test part 2 on example input"""
    expected = 64
    ret = solve_part_two(
        parse(example_data),
        cycles=1000,
    )
    if expected is None:
        pytest.skip("Not yet implemented")
    assert ret == expected
