#!/usr/bin/env python
"""Solutions for AoC 1, 2024."""
# Created: 2024-12-01 11:06:52.879085

# Standard library imports
from aocd.models import Puzzle, default_user
from collections import Counter
from rich import print


def parse(input_data):
    """Transform the data"""
    left_vals, right_vals = [], []
    for line in input_data.splitlines():
        left, right = line.split(" ")[0], line.split(" ")[-1]
        left_vals.append(int(left))
        right_vals.append(int(right))
    left_vals = sorted(left_vals)
    right_vals = sorted(right_vals)
    return left_vals, right_vals


def solve_part_one(input_data):
    """Solve part one."""
    left_vals, right_vals = input_data
    answer = 0
    for left, right in zip(left_vals, right_vals):
        delta = abs(left - right)
        answer += delta
    return answer


def solve_part_two(input_data):
    """Solve part two."""
    left_vals, right_vals = input_data
    answer = 0
    right_vals = Counter(right_vals)
    for entry in left_vals:
        answer += entry * right_vals[entry]
    return answer


def main():
    puzzle = Puzzle(year=2024, day=1)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2024).get((2024, 1), {})
    if stats.get("a", None) is None:
        answer_a = solve_part_one(parsed_data)
        if answer_a:
            puzzle.answer_a = answer_a
    if stats.get("b", None) is None:
        parsed_data = parse(puzzle.input_data)
        answer_b = solve_part_two(parsed_data)
        if answer_b:
            puzzle.answer_b = answer_b


if __name__ == "__main__":
    main()
