"""Tests for AoC 25, 2021"""

# Standard library imports
import pathlib

# Third party imports
import aoc202125
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202125.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202125.parse(puzzle_input)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 == ...


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc202125.part1(example1) == 58


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc202125.part2(example2) == ...


@pytest.mark.parametrize(
    "step, expected",
    [
        (
            0,
            """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""",
        ),
        (
            1,
            """....>.>v.>
v.v>.>v.v.
>v>>..>v..
>>v>v>.>.v
.>v.v...v.
v>>.>vvv..
..v...>>..
vv...>>vv.
>.v.v..v.v""",
        ),
    ],
)
def test_step(example1, step, expected):
    grid = example1
    for _ in range(step):
        grid.step()
    assert str(grid) == expected


@pytest.mark.parametrize("test_val, expected", [("...>>>>>...", "...>>>>.>..")])
def test_step_right(test_val, expected):
    grid = aoc202125.parse(test_val)
    new_grid, moved = aoc202125.step_right(grid.grid, 1, len(test_val))
    assert aoc202125.grid_to_str(new_grid, 1, len(test_val)) == expected


@pytest.mark.parametrize(("test_val, expected"), [("""...>...
.......
......>
v.....>
......>
.......
..vvv..""", """..vv>..
.......
>......
v.....>
>......
.......
....v..""")])
def test_step_again(test_val, expected):
    grid = aoc202125.parse(test_val)
    grid.step()
    assert str(grid) == expected
