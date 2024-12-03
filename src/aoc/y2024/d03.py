#!/usr/bin/env python
"""Solutions for AoC 3, 2024."""
# Created: 2024-12-03 05:23:39.300292

# Standard library imports
from aocd.models import Puzzle, default_user
import re
from rich import print


def parse(input_data):
    """Transform the data"""
    return input_data


def solve_part_one(input_data):
    """Solve part one."""
    answer = 0
    valid_instruction_regex = r"mul\((\d{1,3}),(\d{1,3})\)"
    matched_instructions = re.finditer(valid_instruction_regex, input_data)
    for match in matched_instructions:
        left, right = int(match.group(1)), int(match.group(2))
        answer += left * right
    return answer


def solve_part_two(input_data):
    """Solve part two."""
    answer = 0
    instructions_regex = r"mul\((\d{1,3}),(\d{1,3})\)|don't\(\)|do\(\)"
    matched_instructions = re.finditer(instructions_regex, input_data)
    instructions_enabled = True
    for match in matched_instructions:
        if match.group() == "don't()":
            instructions_enabled = False
        elif match.group() == "do()":
            instructions_enabled = True
        elif instructions_enabled:
            left, right = int(match.group(1)), int(match.group(2))
            answer += left * right
    return answer


def main():
    puzzle = Puzzle(year=2024, day=3)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2024).get((2024, 3), {})
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
