"""AoC 25, 2021"""

# Standard library imports
import pathlib
import sys
from collections import defaultdict
from dataclasses import dataclass
from aocd import data as input_data, submit


def grid_to_str(grid, row_size, col_size):
    ret = []
    for x in range(row_size):
        ret.append(
            "".join(
                [
                    str(grid[(x, y)]) if grid[(x, y)] != 0 else "."
                    for y in range(col_size)
                ]
            )
        )
    return "\n".join(ret)


def step_right(grid: defaultdict, row_size: int, col_size: int) -> defaultdict:
    """Move entries right.

    Returns grid and moved"""
    moved = False
    new_grid = defaultdict(int)
    for x in range(row_size):
        for y in range(col_size - 1, -1, -1):
            if grid[(x, y)] == ">":
                next_coords = (x, (y + 1) % col_size)
                if grid[next_coords] == 0:
                    new_grid[next_coords] = ">"
                    moved = True
                else:
                    new_grid[(x, y)] = ">"
            else:
                if grid[(x, y)] == 0:
                    continue
                new_grid[(x, y)] = grid[(x, y)]
        # then move southerly
    return new_grid, moved


def step_down(grid: defaultdict, row_size: int, col_size: int) -> defaultdict:
    """Move entries down.

    Returns grid and moved"""
    moved = False
    new_grid = defaultdict(int)
    for x in range(row_size):
        for y in range(col_size):
            val = grid[(x, y)]
            if val == "v":
                next_coords = ((x + 1) % row_size, y)
                if grid[next_coords] == 0:
                    new_grid[next_coords] = val
                    moved = True
                else:
                    new_grid[(x, y)] = val
            else:
                if val != 0:
                    new_grid[(x, y)] = val
    return new_grid, moved


@dataclass
class SeaCucumberGrid:
    grid: defaultdict
    row_size: int = 0
    col_size: int = 0

    def __init__(self, row_size: int = 0, col_size: int = 0) -> None:
        self.grid = defaultdict(int)
        self.row_size = row_size
        self.col_size = col_size

    def step(self) -> bool:
        """Calculate a step.

        Return if any moved

        There are two herds of sea cucumbers sharing the same region; one always moves east (>), while the other always
        moves south (v). Each location can contain at most one sea cucumber; the remaining locations are empty (.). The
        submarine helpfully generates a map of the situation (your puzzle input). For example:
        """
        new_grid, moved_right = step_right(self.grid, self.row_size, self.col_size)
        self.grid = new_grid
        new_grid, moved_down = step_down(self.grid, self.row_size, self.col_size)
        self.grid = new_grid
        return moved_right or moved_down

    def __str__(self) -> str:
        return grid_to_str(self.grid, self.row_size, self.col_size)


def parse(puzzle_input):
    """Parse input.

    Example input:
    v...>>.vv>
    .vv>>.vv..
    >>.>v>...v
    >>v>>.>.v.
    v>v.vv.v..
    >.>>..v...
    .vv..>.>v.
    v.v..>>v.v
    ....v..v.>
    """
    max_row = len(puzzle_input.splitlines())
    max_col = len(puzzle_input.splitlines()[0])
    grid = SeaCucumberGrid(row_size=max_row, col_size=max_col)
    for row, line in enumerate(puzzle_input.splitlines()):
        for col, char in enumerate(line):
            if char != ".":
                grid.grid[(row, col)] = char
    return grid


def part1(data):
    """Solve part 1.

    Every step, the sea cucumbers in the east-facing herd attempt to move forward one location, then the sea cucumbers
    in the south-facing herd attempt to move forward one location. When a herd moves forward, every sea cucumber in the
    herd first simultaneously considers whether there is a sea cucumber in the adjacent location it's facing (even
    another sea cucumber facing the same direction), and then every sea cucumber facing an empty location simultaneously
    moves into that location.

    Due to strong water currents in the area, sea cucumbers that move off the right edge of the map appear on the left
    edge, and sea cucumbers that move off the bottom edge of the map appear on the top edge. Sea cucumbers always check
    whether their destination location is empty before moving, even if that destination is on the opposite side of the
    map:
    Find somewhere safe to land your submarine. What is the first step on which no sea cucumbers move?
    """
    grid = data
    for step in range(2000):
        moved = grid.step()
        if not moved:
            return step+1


def part2(data):
    """Solve part 2"""


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

    answer_a, answer_b = solve(puzzle_input=input_data)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
