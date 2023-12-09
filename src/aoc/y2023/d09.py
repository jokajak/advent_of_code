#!/usr/bin/env python
"""Solutions for AoC 9, 2023."""
# Created: 2023-12-09 10:48:58.950533

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from functools import cache


def parse(input_data):
    """Transform the data"""
    parsed_data = [list(map(int, line.split())) for line in input_data.splitlines()]

    return parsed_data


def next_arithmetic_sequence_value(seq):
    """Get the next value in an arithmetic sequence"""
    total_entries = len(seq)
    return seq[0] + (total_entries) * (seq[1] - seq[0])


def get_differences(seq):
    """Get the difference between every item in a sequence"""
    return [seq[i] - seq[i - 1] for i in range(1, len(seq))]


def get_next_value(seq):
    differences = get_differences(seq)
    if all(differences[0] == diff for diff in differences):  # arithmetic sequence
        return next_arithmetic_sequence_value(seq)
    else:
        next_val = get_next_value(differences)
        return seq[-1] + next_val


def solve_part_one(input_data):
    """Solve part one."""
    answer = 0
    for seq in input_data:
        answer += get_next_value(seq)
    return answer


def get_prev_value(seq):
    differences = get_differences(seq)
    if all(differences[0] == diff for diff in differences):  # arithmetic sequence
        return seq[0] - differences[0]
    else:
        prev_val = get_prev_value(differences)
        return seq[0] - prev_val


def solve_part_two(input_data):
    """Solve part two."""
    answer = 0
    for seq in input_data:
        answer += get_prev_value(seq)
    return answer


def main():
    puzzle = Puzzle(year=2023, day=9)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 9), {})
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
