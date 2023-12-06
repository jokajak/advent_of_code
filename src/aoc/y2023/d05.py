#!/usr/bin/env python
"""Solutions for AoC 5, 2023."""
# Created: 2023-12-05 08:51:39.495463

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print


categories = {}


def parse_map(input_data):
    """Parse a map input"""
    left_map, right_map = {}, {}
    for line in input_data:
        left_start, right_start, map_range = line.split(" ")
        left_start, right_start, map_range = (
            int(left_start),
            int(right_start),
            int(map_range),
        )
        for step in range(map_range):
            right_map[right_start + step] = left_start + step
    return left_map, right_map


def parse(input_data):
    """Transform the data.


    The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into
    numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert
    a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil
    to use with which seeds, which water to use with which fertilizer, and so on.

    ```
    seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4
    ```
    """
    input_lines = input_data.splitlines()
    seeds = input_lines.pop(0)  # strip the first line
    maps = []
    left_map = {}
    right_map = {}
    for line in input_lines:
        if line == "":  # end of the section
            maps.append(right_map)
            left_map = {}
            right_map = {}
            continue
        if line.endswith("map:"):
            left, right = (
                line.split(" ")[0].split("-")[0],
                line.split(" ")[0].split("-")[2],
            )
            continue
        left_start, right_start, map_range = line.split(" ")
        left_start, right_start, map_range = (
            int(left_start),
            int(right_start),
            int(map_range),
        )
        for step in range(map_range):
            right_map[right_start + step] = left_start + step
        # add the map to the list of maps
    return seeds, maps


def solve_part_one(input_data):
    """Solve part one.

    What is the lowest location number that corresponds to any of the initial seed numbers?
    """
    seeds, maps = input_data
    seeds = seeds.split(":")[1].strip(" ").split(" ")
    seed_values = [int(seed) for seed in seeds]
    for map_entry in maps:
        for seed_index, seed in enumerate(seed_values):
            if seed in map_entry:
                seed_values[seed_index] = map_entry[seed]
    min_value, min_index = min((val, idx) for idx, val in enumerate(seed_values))
    print(seeds)
    print(seeds)
    answer = min_value
    return answer


def solve_part_two(input_data):
    """Solve part two."""
    answer = None
    return answer


def main():
    puzzle = Puzzle(year=2023, day=5)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 5), {})
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
