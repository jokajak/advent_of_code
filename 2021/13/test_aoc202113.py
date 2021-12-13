"""Tests for AoC 13, 2021"""

# Standard library imports
import pathlib

# Third party imports
import aoc202113
import pytest
from collections import defaultdict

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202113.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202113.parse(puzzle_input)


def test_dict_to_grid(example1):
    coords, _ = example1
    assert aoc202113.dict_to_grid(coords, printable=True) == [
        "...#..#..#.",
        "....#......",
        "...........",
        "#..........",
        "...#....#.#",
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
        ".#....#.##.",
        "....#......",
        "......#...#",
        "#..........",
        "#.#........",
    ]


def convert_print_to_grid(printable_view: str):
    ret = []
    for line in printable_view.splitlines():
        new_row = [True if col == "#" else False for col in line]
        ret.append(new_row)
    return ret


def test_vertical_fold():
    start_grid = """#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
..........."""
    end_grid = """#####
#...#
#...#
#...#
#####
.....
....."""
    start_grid = convert_print_to_grid(start_grid)
    end_grid = convert_print_to_grid(end_grid)
    assert aoc202113.fold_along_y(start_grid, 5) == end_grid


def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 == (
        defaultdict(
            int,
            {
                (6, 10): True,
                (0, 14): True,
                (9, 10): True,
                (0, 3): True,
                (10, 4): True,
                (4, 11): True,
                (6, 0): True,
                (6, 12): True,
                (4, 1): True,
                (0, 13): True,
                (10, 12): True,
                (3, 4): True,
                (3, 0): True,
                (8, 4): True,
                (1, 10): True,
                (2, 14): True,
                (8, 10): True,
                (9, 0): True,
            },
        ),
        [("y", 7), ("x", 5)],
    )


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc202113.part1(example1) == 17


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc202113.part2(example2) == ...
