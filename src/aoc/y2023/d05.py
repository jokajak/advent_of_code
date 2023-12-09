#!/usr/bin/env python
"""Solutions for AoC 5, 2023."""
# Created: 2023-12-05 08:51:39.495463

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from rich.progress import track
from collections import defaultdict
import math
from typing import List, Tuple


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


def get_map_range(input_range, map_values):
    """Given an input range, return the results of the map.

    For example:

    ((11, 20), (1, 5, 10)) -> [(7,15), (16-20)]
    ((79, 93), (52, 50, 48)) -> [(81, 95)]

    This needs to return multiple information to the caller so that I can account for
    the scenario of having an input_range of (1, 50) and two map_values of:
    (5, 10, 5) and (10, 15, 5)

    Therefore it returns a dictionary of:
    mapped:
    unmapped:
    """
    source_beginning, source_end = input_range
    dest_beginning = dest_end = None
    map_dest_start, map_source_start, count = map_values
    map_dest_end, map_source_end = map_dest_start + count, map_source_start + count
    offset = map_dest_start - map_source_start
    # if the start is within range, then we have a new start
    # if the end is within range, then we have a new end
    if map_source_start <= source_beginning < map_source_end:
        dest_beginning = source_beginning + offset
    if map_source_start <= source_end < map_source_end:
        dest_end = source_end + offset
    if dest_beginning and dest_end:  # source is entirely in the map
        return {"mapped": [(dest_beginning, dest_end)]}
    if not (dest_beginning or dest_end):  # not mapped
        return {"unmapped": [(source_beginning, source_end)]}
    else:  # new ranges
        if dest_beginning:
            return {
                "mapped": [(dest_beginning, map_source_end)],
                "unmapped": [(map_source_end + 1, source_end)],
            }
        if dest_end:
            return {
                "unmapped": [(source_beginning, map_source_start)],
                "mapped": [(map_dest_start, dest_end)],
            }
    raise ValueError


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
    seeds, maps = input_data
    seeds = list(map(int, seeds.split(":")[1].strip(" ").split(" ")))

    seed_ranges = []
    for index in range(0, len(seeds), 2):
        seed_ranges.append((seeds[index], seeds[index] + seeds[index + 1]))

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

    # current_location = 1000000

    # I read a clue on subreddit where someone mentioned using ranges
    # The idea is that each map can generate a list of ranges.
    # After performing all maps, find the lowest start value
    ranges = seed_ranges
    for step, mappings in enumerate(maps):
        print(f"{step}: {len(ranges)} ranges")
        new_ranges = []
        for source_range in ranges:
            for map_entry in mappings:
                ret = get_map_range(source_range, map_entry)
                if ret["mapped"]:
                    new_ranges.extend(ret["mapped"])


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
