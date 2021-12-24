"""Tests for AoC 18, 2021"""

# Standard library imports
import pathlib

# Third party imports
import aoc202118
import pytest
from aoc202118 import SnailfishNumber, list_to_str, str_to_list

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202118.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202118.parse(puzzle_input)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 == ...


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc202118.part1(example1) == 4140


def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc202118.part2(example2) == 3993


@pytest.mark.parametrize(
    "test_val, expected",
    [
        (
            "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]",
            ("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]", True),
        ),
        (
            "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]",
            ("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]", True),
        ),
        ("[7,[6,[5,[4,[3,2]]]]]", ("[7,[6,[5,[7,0]]]]", True)),
        ("[[[[[9,3],4]]]]", ("[[[[0,7]]]]", True)),
        ("[[[[[9,8],1],2],3],4]", ("[[[[0,9],2],3],4]", True)),
        ("[[[[0,7]]]]", ("[[[[0,7]]]]", False)),
    ],
)
def test_explode(test_val, expected):
    ret, exploded = aoc202118.explode_snailfish_number(test_val)
    assert aoc202118.list_to_str(ret), exploded == expected


@pytest.mark.parametrize(
    "test_val, expected",
    [
        (
            "[[[[[9,8],1],2],3],4]",
            ["[", "[", "[", "[", "[", 9, 8, "]", 1, "]", 2, "]", 3, "]", 4, "]"],
        ),
    ],
)
def test_str_to_list(test_val, expected):
    assert aoc202118.str_to_list(test_val) == expected


@pytest.mark.parametrize(
    "expected, test_val",
    [
        (
            "[[[[[9,8],1],2],3],4]",
            ["[", "[", "[", "[", "[", 9, 8, "]", 1, "]", 2, "]", 3, "]", 4, "]"],
        ),
    ],
)
def test_list_to_str(test_val, expected):
    assert aoc202118.list_to_str(test_val) == expected


@pytest.mark.parametrize(
    "test_val, expected",
    [("[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")],
)
def test_split(test_val, expected):
    ret, split = aoc202118.split_snailfish_number(test_val)
    assert aoc202118.list_to_str(ret) == expected


@pytest.mark.parametrize(
    "test_val, expected",
    [
        ("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
        ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
    ],
)
def test_reduce(test_val, expected):
    fish = SnailfishNumber(test_val)
    fish.reduce()
    assert str(fish) == expected


@pytest.mark.parametrize(
    "test_val, expected",
    [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]", 4140),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
    ],
)
def test_magnitude(test_val, expected):
    fish = SnailfishNumber(test_val)
    assert fish.magnitude == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
        ),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", "[5,5]", "[[[[3,0],[5,3]],[4,4]],[5,5]]"),
    ],
)
def test_add(left, right, expected):
    left = SnailfishNumber(left)
    left += SnailfishNumber(right)
    left.reduce()
    assert str(left) == expected


@pytest.mark.parametrize(
    "list_in, expected",
    [
        (
            """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]""",
            "[[[[3,0],[5,3]],[4,4]],[5,5]]",
        ),
        (
            """[1,1]
[2,2]
[3,3]
[4,4]""",
            "[[[[1,1],[2,2]],[3,3]],[4,4]]",
        ),
        (
            """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]""",
            "[[[[5,0],[7,4]],[5,5]],[6,6]]",
        ),
        ("""[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""", "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"),
        ("""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""", "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"),
    ],
)
def test_process_list(list_in, expected):
    data = []
    for line in list_in.splitlines():
        data.append(line)
    fish = SnailfishNumber(data[0])
    for line in data[1:]:
        print(str(fish))
        fish.reduce()
        fish += SnailfishNumber(line)
    fish.reduce()
    print(str(fish))
    assert str(fish) == expected
