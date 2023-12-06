#!/usr/bin/env python
"""Solutions for AoC 3, 2023."""
# Created: 2023-12-03 21:23:10.649431

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from collections import defaultdict


def parse(input_data):
    parsed_data = defaultdict(lambda: ".")
    for row_idx, row in enumerate(input_data.splitlines()):
        for column, value in enumerate(row):
            try:
                parsed_data[(row_idx, column)] = int(value)
            except ValueError:
                parsed_data[(row_idx, column)] = value
    return parsed_data


def get_number(grid, coordinate):
    row, center_col = coordinate
    iter = 0
    num = []
    # look left
    col = center_col - 1
    val = grid[(row, col)]
    # print(f"coordinate: {coordinate} row: {row} col: {col}")
    while isinstance(val, int) and iter < 150:
        # print(f"val: {val}, str(val): {str(val)}")
        num.insert(0, str(val))
        col = col - 1
        val = grid[(row, col)]
        iter += 1
    # move back to the right one
    # because the value isn't an int
    col = col + 1  # move back to the right one
    # print(f"grid[({row}, {center_col})]: {grid[(row, center_col)]}")
    num.append(str(grid[(row, center_col)]))
    end_col = center_col + 1
    iter = 0
    while isinstance(grid[(row, end_col)], int) and iter < 150:
        val = grid[(row, end_col)]
        num.append(str(val))
        end_col = end_col + 1
        iter += 1
    # print(num)
    val = int("".join(num))
    return (row, col), val


def find_numbers_around_symbol(grid, coordinate):
    # fmt: off
    deltas = [
        (-1, 1), (0, 1), (1, 1),
        (-1, 0), (0, 0), (1, 0),
        (-1, -1), (0, -1), (1, -1),
    ]
    # fmt: on
    ret = []
    row, column = coordinate
    for delta_x, delta_y in deltas:
        val = grid[(row + delta_y, column + delta_x)]
        if isinstance(val, int):
            start_coordinate, number = get_number(
                grid, (row + delta_y, column + delta_x)
            )
            ret.append((start_coordinate, number))
    return ret


def solve_part_one(input_data):
    """Solve part one."""
    grid = input_data
    part_numbers = {}
    # consume the list of keys
    coordinates = list(grid.keys())
    for coordinate in coordinates:
        value = grid[coordinate]
        if value != '.' and not isinstance(value, int):
            # must be a symbol
            numbers = find_numbers_around_symbol(grid, coordinate)
            for coordinate, value in numbers:
                part_numbers[coordinate] = value
    answer = sum(part_numbers.values())
    return answer


def solve_part_two(input_data):
    """Solve part two."""
    answer = 0
    grid = input_data
    # consume the list of keys
    coordinates = list(grid.keys())
    for coordinate in coordinates:
        value = grid[coordinate]
        if value == "*":
            # must be a symbol
            numbers = find_numbers_around_symbol(grid, coordinate)
            unique_coordinates = {}
            for coordinate, value in numbers:
                unique_coordinates[coordinate] = value
            if len(unique_coordinates) == 2:
                gear_ratio = 1
                for value in unique_coordinates.values():
                    gear_ratio *= value
                answer += gear_ratio
    return answer


def main():
    puzzle = Puzzle(year=2023, day=3)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 3), {})
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
