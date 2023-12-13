#!/usr/bin/env python
"""Solutions for AoC 11, 2023."""
# Created: 2023-12-11 21:14:18.713063

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from rich.progress import track
from collections import defaultdict
from itertools import combinations


def print_galaxy(galaxy_map):
    rows = max(galaxy_map.keys())
    columns = max(max(row.keys() for row in galaxy_map.values()))
    for row in range(rows):
        row_print = [
            galaxy_map.get(row, {}).get(column, ".") for column in range(columns)
        ]
        print("".join(row_print))


def parse(input_data):
    """Transform the data

    Given an array of . and #, store the coordinates of the #"""
    parsed_data = defaultdict(dict)
    for row_index, row in enumerate(input_data.splitlines()):
        for column_index, value in enumerate(row):
            if value == "#":
                parsed_data[row_index][column_index] = "#"
    return parsed_data


def expand_graph(input_data, expansion_rate=1):
    """Calculate coordinates in a galaxy.

    Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or
    columns that contain no galaxies should all actually be twice as big.
    """

    # I don't understand this
    # but it works per https://www.reddit.com/r/adventofcode/comments/18fzv4k/2023_day_11_part_2_how_to_approach_the_challenge/
    if expansion_rate > 1:
        expansion_rate -= 1
    row_offset = column_offset = 0
    populated_columns = set()
    populated_rows = input_data.keys()
    for row_index, row in input_data.items():
        populated_columns.update(row.keys())

    populated_columns = sorted(populated_columns)
    min_column = populated_columns[0]

    column_mapping = {}
    column_offset = -1 * min_column  # make the first column 0
    next_column_value = 0
    for column_index, column in enumerate(populated_columns):
        column_mapping[column] = next_column_value
        if column_index == len(populated_columns) - 1:
            # don't look at the next column, we've reviewed them all
            break
        next_column = populated_columns[column_index + 1]
        delta = next_column - column
        if delta != 1:
            # with expansion rate 1:
            # 1 -> 3 becomes 1 -> 4 if 2 is empty, offset = 3 - 1 - 1 = 1
            # 1 -> 2 becomes 1 -> 2: 1 * 1 + 1 + 0 = 2
            # 1 -> 4 becomes 1 -> 6 if 2,3 are empty, offset = 4 - 1 - 1 = 2
            # with expansion rate 5:
            # 1 -> 3 becomes 1 -> 7 if 2 is empty, offset = (delta-1) * rate + delta + offset = (1) * 5 + 2 + 0 = 7
            # offset += (delta - 1) * rate
            # 1 -> 4 becomes 1 -> 24 if 2,3 are empty, offset = 20
            column_offset += (delta - 1) * expansion_rate
            print(f"{next_column} missing, column_offset: {column_offset}")

        next_column_value = next_column + column_offset
        print(f"next_column_value: {next_column_value}")
    print(f"Column offsets: {column_mapping}")

    row_mapping = {}
    populated_rows = sorted(populated_rows)
    row_offset = -1 * populated_rows[0]
    for row_index, row in enumerate(populated_rows):
        row_mapping[row] = row + row_offset
        if row_index == len(populated_rows) - 1:
            # don't look at the next row, we've reviewed them all
            break
        next_row = populated_rows[row_index + 1]
        delta = next_row - row
        if delta != 1:
            row_offset += (delta - 1) * expansion_rate
    print(f"Row offsets: {row_mapping}")

    expanded_graph = {}

    for row_index, row in input_data.items():
        new_row = row_mapping.get(row_index, row_index)
        expanded_graph[new_row] = {}
        new_row = expanded_graph[new_row]
        for column in row.keys():
            new_column = column_mapping.get(column, column)
            new_row[new_column] = "#"

    return expanded_graph


def solve_part_one(input_data):
    """Solve part one."""
    answer = 0
    coordinates = []
    print(input_data)
    expanded_graph = expand_graph(input_data)
    for row_index, row in expanded_graph.items():
        for column_index in row.keys():
            coordinates.append((row_index, column_index))

    for left, right in track(combinations(coordinates, 2)):
        x1, y1 = left
        x2, y2 = right
        # Calculate the manhattan distance
        answer += abs(x2 - x1) + abs(y2 - y1)

    return answer


def solve_part_two(input_data, expansion_rate=1000000):
    """Solve part two."""
    answer = 0
    coordinates = []
    expanded_graph = expand_graph(input_data, expansion_rate=expansion_rate)
    for row_index, row in expanded_graph.items():
        for column_index in row.keys():
            coordinates.append((row_index, column_index))

    for left, right in track(combinations(coordinates, 2)):
        x1, y1 = left
        x2, y2 = right
        # Calculate the manhattan distance
        answer += abs(x2 - x1) + abs(y2 - y1)

    return answer


def main():
    puzzle = Puzzle(year=2023, day=11)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 11), {})
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
