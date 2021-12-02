"""AoC 1, 2021"""

# Standard library imports
import pathlib
import sys

from aocd import numbers  # like [int(n) for n in data.splitlines()]


def parse(puzzle_input):
    """Parse input"""
    entries = []
    for line in puzzle_input.split("\n"):
        if line != "":
            entries.append(int(line))
    return entries


def part1(data):
    """Solve part 1"""
    previous_line = 0
    # Start at -1 so that the first line doesn't count
    number_increased = -1
    for line in data:
        # print("%d + %d = %d" % (num_one, num_two, num_one + num_two))
        if line > previous_line:
            number_increased += 1
        previous_line = line
    return number_increased


def part2(data):
    """Solve part 2"""
    index = 3
    last_depth = 0
    # Start at -1 so that the first line doesn't count
    number_increased = 0
    while index < len(data):
        current_depth = sum(data[index - 3 : index])
        if current_depth > last_depth:
            number_increased += 1
        last_depth = current_depth
        index += 1
    return number_increased


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
