"""Tests for AoC 11, 2021"""

# Standard library imports
import pathlib

# Third party imports
import aoc202111
from aoc202111 import OctopusGrid, dict_to_grid, grid_to_dict
from collections import defaultdict
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202111.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202111.parse(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 == [
        [5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
        [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
        [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
        [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
        [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
        [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
        [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
        [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
        [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
        [5, 2, 8, 3, 7, 5, 1, 5, 2, 6],
    ]


def test_print_grid():
    """Verify grid output is correct."""
    grid = defaultdict(
        int,
        {
            (0, 0): 8,
            (0, 1): 9,
            (0, 2): 0,
            (1, 0): 9,
            (1, 1): 9,
            (1, 2): 0,
            (2, 0): 0,
            (2, 1): 0,
            (2, 2): 0,
        },
    )
    assert (
        OctopusGrid.display(grid)
        == """8900000000
9900000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000"""
    )


def test_grid_to_dict():
    """Verify converting a grid made of lists to a defaultdict"""
    # fmt: off
    start_grid = [
        [8, 9, 0],
        [9, 9, 0],
        [0, 0, 0]

    ]
    end_dict = defaultdict(
        int,
        {
            (0, 0): 8,
            (0, 1): 9,
            (0, 2): 0,
            (1, 0): 9,
            (1, 1): 9,
            (1, 2): 0,
            (2, 0): 0,
            (2, 1): 0,
            (2, 2): 0,
        },
    )
    # fmt: on
    assert aoc202111.grid_to_dict(start_grid) == end_dict


def test_dict_to_grid():
    """Verify defaultdict to grid made of lists works"""
    # fmt: off
    end_grid = [
        [8, 9, 0],
        [9, 9, 0],
        [0, 0, 0]

    ]
    start_dict = defaultdict(
        int,
        {
            (0, 0): 8,
            (0, 1): 9,
            (0, 2): 0,
            (1, 0): 9,
            (1, 1): 9,
            (1, 2): 0,
            (2, 0): 0,
            (2, 1): 0,
            (2, 2): 0,
        },
    )
    # fmt: on
    assert aoc202111.dict_to_grid(start_dict, grid_size=(3, 3)) == end_grid


def test_one_corner_flash():
    """Verify corner flashes happen properly."""
    # fmt: off
    start_grid = aoc202111.grid_to_dict([
            [8, 9, 0],
            [9, 9, 0],
            [0, 0, 0]

        ])
    end_grid = aoc202111.grid_to_dict([
            [0, 0, 3],
            [0, 0, 3],
            [3, 3, 2]

        ])
    # fmt: on
    assert OctopusGrid.step_grid(start_grid, (3, 3)) == (end_grid, 4)


def test_corner_flash():
    """Verify corner flashes happen properly."""
    # fmt: off
    assert OctopusGrid.step_grid(aoc202111.grid_to_dict([
        [8, 9, 0],
        [9, 9, 0],
        [0, 0, 0]
    ]), (3, 3)) == (aoc202111.grid_to_dict([
        [0, 0, 3],
        [0, 0, 3],
        [3, 3, 2],
    ]), 4)
    assert OctopusGrid.step_grid(aoc202111.grid_to_dict([
        [0, 9, 8],
        [0, 9, 9],
        [0, 0, 0]
    ]), (3, 3)) == (aoc202111.grid_to_dict([
        [3, 0, 0],
        [3, 0, 0],
        [2, 3, 3],
    ]), 4)

    assert OctopusGrid.step_grid(aoc202111.grid_to_dict([
        [0, 0, 0],
        [0, 9, 9],
        [0, 9, 8]
    ]), (3, 3)) == (aoc202111.grid_to_dict([
        [2, 3, 3],
        [3, 0, 0],
        [3, 0, 0],
    ]), 4)

    assert OctopusGrid.step_grid(aoc202111.grid_to_dict([
        [0, 0, 0],
        [9, 9, 0],
        [8, 9, 0]
    ]), (3, 3)) == (aoc202111.grid_to_dict([
        [3, 3, 2],
        [0, 0, 3],
        [0, 0, 3],
    ]), 4)
    # fmt: on


def test_center_flash():
    assert OctopusGrid.step_grid(aoc202111.grid_to_dict([
        [9, 9, 9],
        [9, 1, 9],
        [9, 9, 9]
    ]), (3, 3)) == (aoc202111.grid_to_dict([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]), 9)


def test_rolling_flash():
    assert OctopusGrid.step_grid(aoc202111.grid_to_dict([
        [8, 7],
        [9, 6],
    ]), (2, 2)) == (aoc202111.grid_to_dict([
        [0, 0],
        [0, 0],
    ]), 4)


def test_no_flash():
    assert OctopusGrid.step_grid(aoc202111.grid_to_dict([
        [0, 0],
        [0, 0],
    ]), (2, 2)) == (aoc202111.grid_to_dict([
        [1, 1],
        [1, 1],
    ]), 0)


def test_part1_example1_steps():
    assert OctopusGrid.step_grid(aoc202111.grid_to_dict([
        [5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
        [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
        [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
        [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
        [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
        [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
        [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
        [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
        [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
        [5, 2, 8, 3, 7, 5, 1, 5, 2, 6],
    ])) == (aoc202111.grid_to_dict([
        [6, 5, 9, 4, 2, 5, 4, 3, 3, 4],
        [3, 8, 5, 6, 9, 6, 5, 8, 2, 2],
        [6, 3, 7, 5, 6, 6, 7, 2, 8, 4],
        [7, 2, 5, 2, 4, 4, 7, 2, 5, 7],
        [7, 4, 6, 8, 4, 9, 6, 5, 8, 9],
        [5, 2, 7, 8, 6, 3, 5, 7, 5, 6],
        [3, 2, 8, 7, 9, 5, 2, 8, 3, 2],
        [7, 9, 9, 3, 9, 9, 2, 2, 4, 5],
        [5, 9, 5, 7, 9, 5, 9, 6, 6, 5],
        [6, 3, 9, 4, 8, 6, 2, 6, 3, 7],
    ]), 0)

    assert OctopusGrid.step_grid(grid_to_dict([
        [6, 5, 9, 4, 2, 5, 4, 3, 3, 4],
        [3, 8, 5, 6, 9, 6, 5, 8, 2, 2],
        [6, 3, 7, 5, 6, 6, 7, 2, 8, 4],
        [7, 2, 5, 2, 4, 4, 7, 2, 5, 7],
        [7, 4, 6, 8, 4, 9, 6, 5, 8, 9],
        [5, 2, 7, 8, 6, 3, 5, 7, 5, 6],
        [3, 2, 8, 7, 9, 5, 2, 8, 3, 2],
        [7, 9, 9, 3, 9, 9, 2, 2, 4, 5],
        [5, 9, 5, 7, 9, 5, 9, 6, 6, 5],
        [6, 3, 9, 4, 8, 6, 2, 6, 3, 7],
    ])) == (grid_to_dict([
        [8, 8, 0, 7, 4, 7, 6, 5, 5, 5],
        [5, 0, 8, 9, 0, 8, 7, 0, 5, 4],
        [8, 5, 9, 7, 8, 8, 9, 6, 0, 8],
        [8, 4, 8, 5, 7, 6, 9, 6, 0, 0],
        [8, 7, 0, 0, 9, 0, 8, 8, 0, 0],
        [6, 6, 0, 0, 0, 8, 8, 9, 8, 9],
        [6, 8, 0, 0, 0, 0, 5, 9, 4, 3],
        [0, 0, 0, 0, 0, 0, 7, 4, 5, 6],
        [9, 0, 0, 0, 0, 0, 0, 8, 7, 6],
        [8, 7, 0, 0, 0, 0, 6, 8, 4, 8],
    ]), 35)


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc202111.part1(example1) == 1656


def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc202111.part2(example2) == 195
