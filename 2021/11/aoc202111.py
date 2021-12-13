"""AoC 11, 2021"""

# Standard library imports
import pathlib
import sys
from copy import deepcopy
from collections import defaultdict
from aocd import data as input_data, submit


# fmt: off
neighboring_cells = [(-1, -1), (-1, 0), (-1, 1),
                     ( 0, -1),          ( 0, 1),  # noqa: E201
                     ( 1, -1), ( 1, 0), ( 1, 1)]  # noqa: E201
# fmt: on


grid_size = 10, 10
class OctopusGrid(object):
    """Representation of an Octopus Grid

    The energy level of each octopus is a value between 0 and 9. Here, the top-left octopus has an energy level of 5,
    the bottom-right one has an energy level of 6, and so on.

    You can model the energy levels and flashes of light in steps. During a single step, the following occurs:

    First, the energy level of each octopus increases by 1. Then, any octopus with an energy level greater than 9
    flashes. This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally
    adjacent. If this causes an octopus to have an energy level greater than 9, it also flashes. This process continues
    as long as new octopuses keep having their energy level increased beyond 9. (An octopus can only flash at most once
    per step.) Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its
    energy to flash. Adjacent flashes can cause an octopus to flash on a step even if it begins that step with very
    little energy. Consider the middle octopus with 1 energy in this situation:
    """

    def __init__(self, grid: list) -> None:
        self.grid = deepcopy(grid)

    @staticmethod
    def increase_energy(grid: list, size: tuple = grid_size) -> defaultdict:
        max_x, max_y = size
        next_grid = defaultdict(int)
        for row in range(max_y):
            for col in range(max_x):
                new_val = grid[(row, col)] + 1
                next_grid[(row, col)] = new_val
        return next_grid

    @staticmethod
    def step_grid(grid: list, size: tuple = grid_size) -> list:
        """Calculate next step in the grid.

        * First, the energy level of each octopus increases by 1.
        * Then, any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent
          octopuses by 1, including octopuses that are diagonally adjacent. If this causes an octopus to have an energy
          level greater than 9, it also flashes. This process continues as long as new octopuses keep having their
          energy level increased beyond 9. (An octopus can only flash at most once per step.)
        * Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy
          to flash.
        """
        next_grid = defaultdict(int)
        tmp_grid = defaultdict(int)
        max_x, max_y = size
        grid_flashes = defaultdict(int)
        tmp_grid = OctopusGrid.increase_energy(grid, size=size)
        flashed = True
        while flashed:
            flashed = False
            for row in range(max_y):
                for col in range(max_x):
                    current_val = tmp_grid[(row, col)]
                    if current_val >= 10 and grid_flashes[(row, col)] == 0:
                        grid_flashes[(row, col)] = 1
                        flashed = True
                        for nr in range(row-1, row+2):
                            for nc in range(col-1, col+2):
                                tmp_grid[(nr, nc)] = min(tmp_grid[(nr, nc)] + 1, 10)  # ensure maximum value is 10
                        tmp_grid[(row, col)] = min(current_val, 10)  # ensure maximum value is 10
        # reset all flashes to 0 by taking modulus 10
        for row in range(max_y):
            for col in range(max_x):
                next_grid[(row, col)] = tmp_grid[(row, col)] % 10

        return next_grid, sum([v for k, v in grid_flashes.items()])

    @staticmethod
    def display(grid):
        """Display the grid of characters."""
        ret = []
        max_x, max_y = grid_size
        for row in range(max_y):
            ret.append("".join(str(grid[(row, col)]) for col in range(max_x)))
        return "\n".join(ret)


def parse(puzzle_input):
    """Parse input"""
    return [[int(entry) for entry in line] for line in puzzle_input.splitlines()]


def grid_to_dict(input):
    grid = defaultdict(int, {})
    for row, entry in enumerate(input):
        for col, val in enumerate(entry):
            grid[(row, col)] = val
    return grid


def dict_to_grid(input, grid_size=grid_size):
    grid = []
    max_x, max_y = grid_size
    for row in range(max_y):
        new_row = []
        for col in range(max_x):
            new_row.append(input[row, col])
        grid.append(new_row)
    return grid


def part1(data):
    """Solve part 1"""
    grid = grid_to_dict(data)
    total_flashes = 0
    for _ in range(100):
        next_grid, flashes = OctopusGrid.step_grid(grid)
        total_flashes += flashes
        grid = next_grid
    return total_flashes


def part2(data):
    """Solve part 2

    If you can calculate the exact moments when the octopuses will all flash simultaneously, you should be able to
    navigate through the cavern. What is the first step during which all octopuses flash?
    """
    grid = grid_to_dict(data)
    for iteration in range(1000):
        next_grid, flashes = OctopusGrid.step_grid(grid)
        if all([next_grid[(r, c)] == next_grid[(0, 0)] for r in range(10) for c in range(10)]):
            return iteration + 1
        grid = next_grid
    return


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    answer_a, answer_b = solve(puzzle_input=input_data)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
