#!/usr/bin/env python
"""Solutions for AoC 5, 2023."""
# Created: 2023-12-05 08:51:39.495463

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from rich.progress import track
from collections import defaultdict
import math


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
    entries = []
    for line in input_lines:
        if line == "":  # end of the section
            if len(entries):
                maps.append(entries)
                entries = []
            continue
        if line.endswith("map:"):
            continue
        left_start, right_start, map_range = line.split(" ")
        left_start, right_start, map_range = (
            int(left_start),
            int(right_start),
            int(map_range),
        )
        entries.append((left_start, right_start, map_range))
    maps.append(entries)
    return seeds, maps


def lookup_next_val(current_value, maps):
    for dest, source, map_range in maps:
        if source <= current_value < source + map_range:
            offset = current_value - source
            return offset + dest
    return current_value


def print_paths(seed_paths):
    for seed_index, path in seed_paths.items():
        print(f"{seed_index}: {'->'.join(map(str, path))}")


def solve_part_one(input_data):
    """Solve part one.

    What is the lowest location number that corresponds to any of the initial seed numbers?
    """
    seeds, maps = input_data
    seeds = seeds.split(":")[1].strip(" ").split(" ")
    seed_values = [int(seed) for seed in seeds]
    seed_paths = defaultdict(list)
    for seed_index, seed in enumerate(seed_values):
        print(f"Getting seed location: {seed}")
        for map_entry in maps:
            seed_paths[seed_index].append(seed_values[seed_index])
            seed_values[seed_index] = lookup_next_val(
                seed_values[seed_index], map_entry
            )
            print(f"Seed value: {seed_values[seed_index]}")
        print(f"Location: {seed_values[seed_index]}")
    print_paths(seed_paths)
    min_value, min_index = min((val, idx) for idx, val in enumerate(seed_values))
    answer = min_value
    return answer


def solve_part_two(input_data):
    """Solve part two.

    The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and
    the second value is the length of the range. So, in the first line of the example above:

    seeds: 79 14 55 13

    This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number
    79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values:
    55, 56, ..., 66, 67.

    Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.
    """
    # seeds, maps = input_data
    seeds = list(map(int, seeds.split(":")[1].strip(" ").split(" ")))
    # seed_values = []
    # for i in range(0, math.floor((len(seeds) / 2)), 2):
    #     for s in range(seeds[i], seeds[i] + seeds[i + 1]):
    #         seed_values.append(s)
    # This approach technically works but is too slow (>24 hours)
    # print(len(seed_values)) -> 926074368
    # that number is too many to iterate through the full map
    # can I calculate the value of the location formulaicly?
    # I feel like I should be able to use the fact that if a number isn't specifically mapped it is itself
    # I read a clue on reddit to map from the location back to an input and start from 0
    # for seed_index in track(range(len(seed_values))):
    #     # print(f"Getting seed location: {seed_values[seed_index]}")
    #     for map_entry in maps:
    #         seed_paths[seed_index].append(seed_values[seed_index])
    #         seed_values[seed_index] = lookup_next_val(
    #             seed_values[seed_index], map_entry
    #         )
    #         # print(f"Seed value: {seed_values[seed_index]}")
    #     # print(f"Location: {seed_values[seed_index]}")
    # print_paths(seed_paths)
    # min_value, min_index = min((val, idx) for idx, val in enumerate(seed_values))
    # answer = min_value
    # return answer
    # Start with this end location as being too low

    current_location = 1000000

    def lookup_next_val(current_value, maps):
        for dest, source, map_range in maps:
            if source <= current_value < source + map_range:
                offset = current_value - source
                return offset + dest
        return current_value

    seed_ranges = []
    for i in range(0, math.floor((len(seeds) / 2)), 2):
        seed_ranges.append((seeds[i], seeds[i] + seeds[i + 1]))

    maps = reversed(maps)
    iter = 0
    while iter < 100000000:
        iter += 1
        current_location += 1


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
