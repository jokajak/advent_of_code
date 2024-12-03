#!/usr/bin/env python
"""Solutions for AoC 2, 2024."""
# Created: 2024-12-02 10:27:16.376558

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print


def parse(input_data):
    """Transform the data"""
    for line in input_data.splitlines():
        yield line.split(" ")


def solve_part_one(input_data):
    """Solve part one."""
    answer = 0
    for line in input_data:
        if is_safe(line):
            answer += 1
    return answer


def is_safe(line):
    """Check if the line is safe."""
    increasing = None
    for i in range(len(line) - 1):
        current, next = int(line[i]), int(line[i + 1])
        if increasing is None:
            if current > next:
                increasing = False
            else:
                increasing = True
        delta = abs(current - next)
        if delta == 0 or delta > 3:
            return False
        if current > next and increasing:
            break
        if current < next and not increasing:
            break
    else:
        return True


def can_be_safe(line):
    """Check if a line can be safe"""
    for i in range(len(line)):
        test_line = line.copy()
        del test_line[i]
        if is_safe(test_line):
            return True
    else:
        return False


def solve_part_two(input_data):
    """Solve part two."""
    answer = 0
    for line in input_data:
        if is_safe(line):
            answer += 1
        else:
            if can_be_safe(line):
                answer += 1
    return answer


def main():
    puzzle = Puzzle(year=2024, day=2)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2024).get((2024, 2), {})
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
