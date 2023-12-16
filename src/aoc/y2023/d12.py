#!/usr/bin/env python
"""Solutions for AoC 12, 2023."""
# Created: 2023-12-15 08:03:54.717218

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print


def parse(input_data):
    """Transform the data"""
    return input_data


def solve_part_one(input_data):
    """Solve part one.

    
    """
    answer = None
    return answer


def solve_part_two(input_data):
    """Solve part two."""
    answer = None
    return answer


def main():
    puzzle = Puzzle(year=2023, day=12)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 12), {})
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