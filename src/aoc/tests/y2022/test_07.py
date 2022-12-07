#!/usr/bin/env python
"""Tests for AoC 7, 2022"""

from pathlib import PurePath

import pytest

# Third party imports
from aocd.models import Puzzle

from aoc.y2022.communications import Directory, File, get_size, walk_commands
from aoc.y2022.d07 import parse, solve_part_one, solve_part_two


@pytest.fixture
def example_data():
    puzzle = Puzzle(year=2022, day=7)
    example_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
    return example_data


def test_parse_example1(example_data):
    """Test that input is parsed properly"""
    expected = """- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - d.ext (file, size=5626152)
    - d.log (file, size=8033020)
    - j (file, size=4060174)
    - k (file, size=7214296)"""
    res = parse(example_data)
    assert str(res) == expected


def test_directory_str():
    root = Directory(PurePath("/"), parent=None)
    a = Directory(PurePath("/") / "a", root)
    d = Directory(PurePath("/") / "d", root)
    d_log = File(d.path / "d.log", 8033020)
    assert str(root) == "- / (dir)"
    assert str(a) == "  - a (dir)"
    assert str(d) == "  - d (dir)"
    assert str(d_log) == "    - d.log (file, size=8033020)"


def test_directory_size():
    input_data = """$ cd /
$ ls
29116 f"""
    assert solve_part_one(parse(input_data)) == 29116


def test_part1_example1(example_data):
    """Test part 1 on example input"""
    expected = 95437
    assert solve_part_one(parse(example_data)) == expected


def test_part2_example2(example_data):
    """Test part 2 on example input"""
    expected = 24933642
    assert solve_part_two(parse(example_data)) == expected
