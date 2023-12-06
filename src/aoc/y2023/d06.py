#!/usr/bin/env python
"""Solutions for AoC 6, 2023."""
# Created: 2023-12-06 08:19:38.580188

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from rich.progress import track
import functools


def parse(input_data):
    """Transform the data

    Time:      7  15   30
    Distance:  9  40  200

    This document describes three races:

    The first race lasts 7 milliseconds. The record distance in this race is 9 millimeters.
    The second race lasts 15 milliseconds. The record distance in this race is 40 millimeters.
    The third race lasts 30 milliseconds. The record distance in this race is 200 millimeters.
    """
    # assume it's two lines long
    race_times = map(int, input_data.splitlines()[0].split(":")[1].split())
    distances = map(int, input_data.splitlines()[1].split(":")[1].split())

    return race_times, distances


@functools.cache
def calculate_distance(total_time, acceleration_time):
    """Given a time spent accelerating (and not moving), calculate the distance traveled"""
    return acceleration_time * (total_time - acceleration_time)


def solve_part_one(input_data):
    """Solve part one.

    Since the current record for this race is 9 millimeters, there are actually 4 different ways you could win: you
    could hold the button for 2, 3, 4, or 5 milliseconds at the start of the race.

    To see how much margin of error you have, determine the number of ways you can beat the record in each race; in this
    example, if you multiply these values together, you get 288 (4 * 8 * 9).
    """
    answer = 1
    for time_limit, record_distance in zip(input_data[0], input_data[1]):
        ways_to_win = 0
        for acceleration_time in range(time_limit):
            distance = calculate_distance(time_limit, acceleration_time)
            if distance > record_distance:
                ways_to_win += 1
        answer *= ways_to_win
    return answer


def solve_part_two(input_data):
    """Solve part two.

    There's really only one race - ignore the spaces between the numbers on each line.
    """
    answer = 0
    times = int("".join(map(str, input_data[0])))
    distances = int("".join(map(str, input_data[1])))
    # this brute forces the determination from 0 and is inefficient
    # it would be better if I calculated the minimun acceleration time via the derivative
    for acceleration_time in track(range(times)):
        distance = calculate_distance(times, acceleration_time)
        if distance > distances:
            answer += 1
    return answer


def main():
    puzzle = Puzzle(year=2023, day=6)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 6), {})
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
