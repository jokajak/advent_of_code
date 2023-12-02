#!/usr/bin/env python
"""Solutions for AoC 1, 2023."""
# Created: 2023-12-01 06:30:58.232522

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print


def parse(input_data):
    """Transform the data"""
    return input_data.splitlines()


def solve_part_one(input_data):
    """Solve part one."""
    answer = None
    calibration_values = []
    for entry in input_data:
        val = None
        for s in entry:
            if s.isdigit():
                val = s
                break
        else:
            raise
        for s in entry[::-1]:
            if s.isdigit():
                val = f"{val}{s}"
                break
        else:
            raise
        val = int(val)
        calibration_values.append(val)
    answer = sum(calibration_values)
    return answer


def find_first_number(entry):
    """Find the first number in a string"""
    digits = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    ]
    for i in range(len(entry)):
        for digit in digits:
            # print(f"front {entry[i:]} {digit} = {entry[i:].startswith(digit)}")
            if entry[i:].startswith(digit):
                return digit
    else:
        raise


def find_last_number(entry):
    """Find the last number in a string"""
    digits = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    ]
    for i in range(len(entry)):
        idx = i + 1
        for digit in digits:
            print(
                f"back {idx} {entry[-idx::]} {digit} = {entry[-idx::].startswith(digit)}"
            )
            if entry[-idx::].startswith(digit):
                return digit
    else:
        raise


def solve_part_two(input_data):
    """Solve part two."""
    digits = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    ]
    numbers = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
    }
    calibration_values = []
    for entry in input_data:
        first_number = numbers[find_first_number(entry)]
        last_number = numbers[find_last_number(entry)]
        val = int(f"{first_number}{last_number}")
        calibration_values.append(int(val))
    answer = sum(calibration_values)
    return answer


def main():
    puzzle = Puzzle(year=2023, day=1)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 1), {})
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
