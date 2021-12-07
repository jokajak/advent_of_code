"""AoC 7, 2021"""

# Standard library imports
from aocd import data, submit


def parse(puzzle_input):
    """Parse input"""
    return [int(v) for v in puzzle_input.split(",")]


def part1(data):
    """Solve part 1"""
    minimum_fuel_cost = len(data) * len(data)
    for possible_position in range(len(data)):
        total_fuel_cost = 0
        for initial_position in data:
            total_fuel_cost += abs(initial_position - possible_position)
        minimum_fuel_cost = min(total_fuel_cost, minimum_fuel_cost)
    return minimum_fuel_cost


def part2(data):
    """Solve part 2.

    The crabs don't seem interested in your proposed solution. Perhaps you misunderstand crab engineering?

    As it turns out, crab submarine engines don't burn fuel at a constant rate. Instead, each change of 1 step in
    horizontal position costs 1 more unit of fuel than the last: the first step costs 1, the second step costs 2, the
    third step costs 3, and so on.
    """
    minimum_fuel_cost = []
    for possible_position in range(len(data)):
        total_fuel_cost = 0
        for initial_position in data:
            distance = abs(initial_position - possible_position)
            total_fuel_cost += sum([v for v in range(distance + 1)])
        minimum_fuel_cost.append(total_fuel_cost)
    return min(minimum_fuel_cost)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    answer_a, answer_b = solve(puzzle_input=data)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
