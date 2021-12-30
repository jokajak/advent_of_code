"""Tests for AoC 20, 2021"""

# Standard library imports
import pathlib

# Third party imports
import aoc202120
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202120.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202120.parse(puzzle_input)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 == ...


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc202120.part1(example1) == 35


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc202120.part2(example2) == ...


@pytest.mark.parametrize(
    "image, coords, expected_index",
    [
        (
            """#..#.
#....
##..#
..#..
..###""",
            (0, 0),
            34,
        ),
    ],
)
def test_output_pixel_indexing(image, coords, expected_index):
    """Verify output pixel indexing works."""
    input_image = aoc202120.image_str_to_dict(image.splitlines())
    trench_map = aoc202120.TrenchMap([], input_image)
    x, y = coords
    assert trench_map.get_output_pixel_index(x, y)
