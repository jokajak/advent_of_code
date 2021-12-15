"""Tests for AoC 14, 2021"""

# Standard library imports
import pathlib

# Third party imports
import aoc202114
import pytest
from collections import defaultdict

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202114.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202114.parse(puzzle_input)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly"""
    assert example1 == ...


def test_part1_step1(example1):
    polymer_template, rules = example1
    pairs = defaultdict(int)
    # initialize pairs dictionary
    for i in range(len(polymer_template) - 1):
        pairs[polymer_template[i : i + 2]] += 1  # pull out two characters from the string

    expected_polymer = "NCNBCHB"
    expected_pairs = defaultdict(int)
    for i in range(len(expected_polymer) - 1):
        expected_pairs[expected_polymer[i : i + 2]] += 1  # pull out two characters from the string

    expected = defaultdict(int, {
        "NC": 1,
        "CN": 1,
        "NB": 1,
        "BC": 1,
        "CH": 1,
        "HB": 1,
        "CB": 0,
        "NN": 0,
    })

    test_expected = defaultdict(int)
    for k, v in expected.items():
        if v != 0:
            test_expected[k] = v

    assert expected_pairs == test_expected
    ret = aoc202114.process_polymer_change(pairs, rules)
    res_dict = defaultdict(int)
    for k, v in ret.items():
        if v != 0:
            res_dict[k] = v
    assert res_dict == test_expected


def test_part1_step2(example1):
    polymer_template, rules = example1
    pairs = aoc202114.polymer_to_pairs(polymer_template)

    expected = "NBCCNBBBCBHCB"
    expected_pairs = aoc202114.polymer_to_pairs(expected)
    pairs = aoc202114.process_polymer_change(pairs, rules)
    pairs = aoc202114.process_polymer_change(pairs, rules)

    res_dict = defaultdict(int)
    for k, v in pairs.items():
        if v != 0:
            res_dict[k] = v
    assert res_dict == expected_pairs


def strip_defaults(input_dict: defaultdict) -> defaultdict:
    res = defaultdict(int)
    for k, v in input_dict.items():
        if v != 0:
            res[k] = v
    return res


@pytest.mark.parametrize("letters,counts", [("NCNBCHB", defaultdict(int, {"N": 2, "C": 2, "B": 2, "H": 1}))])
def test_letter_counting(letters, counts):
    polymer_pairs = aoc202114.polymer_to_pairs(letters)
    letters = aoc202114.count_letters(polymer_pairs)
    assert letters == counts


def test_part1_example1_step3(example1):
    _, rules = example1
    pairs = aoc202114.polymer_to_pairs("NBCCNBBBCBHCB")
    expected = aoc202114.polymer_to_pairs("NBBBCNCCNBBNBNBBCHBHHBCHB")
    actual = aoc202114.process_polymer_change(pairs, rules)
    actual = strip_defaults(actual)
    assert actual == expected


@pytest.mark.parametrize("steps,expected", [(1, "NCNBCHB"), (2, "NBCCNBBBCBHCB"), (3, "NBBBCNCCNBBNBNBBCHBHHBCHB")])
def test_part1_example1_steps(example1, steps, expected):
    polymer_template, rules = example1
    expected = aoc202114.polymer_to_pairs(expected)
    pairs = aoc202114.polymer_to_pairs(polymer_template)
    actual = aoc202114.iterate_polymer(pairs, rules, steps)
    actual = strip_defaults(actual)
    assert actual == expected


def test_part1_example1(example1):
    """Test part 1 on example input"""
    # assert aoc202114.step(example1, 1) == "NCNBCHB"
    assert aoc202114.part1(example1) == 1588


def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc202114.part2(example2) == 2188189693529
