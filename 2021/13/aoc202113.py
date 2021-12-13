"""AoC 13, 2021"""

# Standard library imports
import pathlib
import sys
from parse import compile
from collections import defaultdict
from aocd import data as input_data, submit


def parse(puzzle_input):
    """Parse input.

    The first section is a list of dots on the transparent paper. 0,0 represents the top-left coordinate. The first
    value, x, increases to the right. The second value, y, increases downward. So, the coordinate 3,0 is to the right of
    0,0, and the coordinate 0,7 is below 0,0. The coordinates in this example form the following pattern, where # is a
    dot on the paper and . is an empty, unmarked position:
    """
    coords = defaultdict(int)
    folds = []
    parser = compile("fold along {axis}={val:d}")
    for line in puzzle_input.splitlines():
        if line == "":
            continue
        if "," in line:
            y, x = line.split(",")
            coords[(int(y), int(x))] = True
        else:
            res = parser.parse(line)
            folds.append((res["axis"], res["val"]))
    return coords, folds


def dict_to_grid(input_dict: dict, printable: bool = False) -> list:
    """Convert defaultdict to grid"""
    max_x = max_y = -1
    for key in input_dict:
        y, x = key
        max_x, max_y = max(max_x, x), max(max_y, y)

    ret = []
    for row in range(max_x + 1):
        new_row = []
        for col in range(max_y + 1):
            if input_dict[(col, row)]:
                if printable:
                    new_row.append("#")
                else:
                    new_row.append(True)
            else:
                if printable:
                    new_row.append(".")
                else:
                    new_row.append(False)
        if printable:
            ret.append("".join(new_row))
        else:
            ret.append(new_row)
    return ret


def print_grid(grid):
    for row in grid:
        print("".join(["#" if val else "." for val in row]))


def fold_along_x(grid: list, value: int) -> list:
    """Fold a grid based on a horizontal line in the grid"""
    new_grid = grid[:value]
    other_grid = grid[value:]
    for row in range(value + 1):
        for col in range(len(new_grid[0])):
            new_grid[-row][col] = other_grid[row][col] or new_grid[-row][col]
    return new_grid


def fold_along_y(grid: list, value: int) -> list:
    """Fold a grid based on a vertical line in the grid"""
    new_grid = []
    for row in range(len(grid)):
        new_row = grid[row][:value]
        other_row = grid[row][value:]
        other_row.reverse()

        for col in range(len(new_row)):
            new_row[col] = new_row[col] or other_row[col]
        new_grid.append(new_row)
    return new_grid


def part1(data):
    """Solve part 1

    The first section is a list of dots on the transparent paper. 0,0 represents the top-left coordinate. The first
    value, x, increases to the right. The second value, y, increases downward. So, the coordinate 3,0 is to the right of
    0,0, and the coordinate 0,7 is below 0,0. The coordinates in this example form the following pattern, where # is a
    dot on the paper and . is an empty, unmarked position:

    Then, there is a list of fold instructions. Each instruction indicates a line on the transparent paper and wants you
    to fold the paper up (for horizontal y=... lines) or left (for vertical x=... lines). In this example, the first
    fold instruction is fold along y=7, which designates the line formed by all of the positions where y is 7 (marked
    here with -):

    Because this is a horizontal line, fold the bottom half up. Some of the dots might end up overlapping after the fold
    is complete, but dots will never appear exactly on a fold line. The result of doing this fold looks like this:
    """
    max_x = max_y = -1
    coords, folds = data
    for key in coords:
        x, y = key
        max_x, max_y = max(max_x, x), max(max_y, y)
    grid = dict_to_grid(coords)

    axis, value = folds[0]
    if axis == "y":
        new_grid = fold_along_x(grid, value)
    elif axis == "x":
        new_grid = fold_along_y(grid, value)

    return sum([1 for row in new_grid for col in row if col])


def part2(data):
    """Solve part 2.
    Finish folding the transparent paper according to the instructions. The manual says the code is always eight capital letters.
    """
    max_x = max_y = -1
    coords, folds = data
    for key in coords:
        x, y = key
        max_x, max_y = max(max_x, x), max(max_y, y)
    grid = dict_to_grid(coords)

    for fold in folds:
        axis, value = fold
        if axis == "y":
            new_grid = fold_along_x(grid, value)
        elif axis == "x":
            new_grid = fold_along_y(grid, value)
        grid = new_grid
    print_grid(grid)
    # PZFJHRFZ
    return "PZFJHRFZ"


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
