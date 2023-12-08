#!/usr/bin/env python
"""Solutions for AoC 8, 2023."""
# Created: 2023-12-08 08:41:12.821648

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print


def parse(input_data):
    """Transform the data"""
    input_data = input_data.splitlines()

    directions = input_data.pop(0)  # get the first line
    input_data.pop(0)  # strip the blank line

    nodes = {}
    for line in input_data:
        node, turns = line.split(" = ")
        turns = turns.replace("(", "").replace(")", "").split(", ")
        nodes[node] = turns

    return directions, nodes


def generate_turns(directions):
    index = 0
    total_directions = len(directions)
    turns = {"L": 0, "R": 1}
    total_steps = 10**10  # 10 raised to the power 10
    for index in range(total_steps):
        yield turns[directions[index % total_directions]]


def solve_part_one(input_data):
    """Solve part one."""
    steps = 0
    directions, nodes = input_data
    current_node = "AAA"
    for turn in generate_turns(directions):
        steps += 1
        current_node = nodes[current_node][turn]
        if current_node == "ZZZ":
            break
    answer = steps
    return answer


def solve_part_two(input_data):
    """Solve part two."""
    answer = None
    return answer


def main():
    puzzle = Puzzle(year=2023, day=8)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 8), {})
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
