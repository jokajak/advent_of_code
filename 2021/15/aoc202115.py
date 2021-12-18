"""AoC 15, 2021"""

# Standard library imports
import pathlib
import sys
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from aocd import data as input_data, submit


def parse(puzzle_input):
    """Parse input"""
    return [[int(v) for v in row] for row in puzzle_input.splitlines()]


def part1(data):
    """Solve part 1.

    The cavern is large, but has a very low ceiling, restricting your motion to two dimensions. The shape of the cavern
    resembles a square; a quick scan of chiton density produces a map of risk level throughout the cave (your puzzle
    input). For example:

    1163751742
    1381373672
    2136511328
    3694931569
    7463417111
    1319128137
    1359912421
    3125421639
    1293138521
    2311944581

    You start in the top left position, your destination is the bottom right position, and you cannot move diagonally.
    The number at each position is its risk level; to determine the total risk of an entire path, add up the risk levels
    of each position you enter (that is, don't count the risk level of your starting position unless you enter it;
    leaving it adds no risk to your total).

    Your goal is to find a path with the lowest total risk.
    """
    grid = Grid(matrix=data)
    start = grid.node(0, 0)
    end = grid.node(len(data) - 1, len(data[0]) - 1)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)
    print("operations:", runs, "path length:", len(path))
    # Ignore the first node because it's not entered
    total_risk = sum([data[coords[1]][coords[0]] for coords in path]) - data[0][0]
    # print(grid.grid_str(path=path, start=start, end=end))
    return total_risk


def expand_map(data):
    """Expand map data.

    The entire cave is actually five times larger in both dimensions than you thought; the area you originally scanned
    is just one tile in a 5x5 tile area that forms the full map. Your original map tile repeats to the right and
    downward; each time the tile repeats to the right or downward, all of its risk levels are 1 higher than the tile
    immediately up or left of it. However, risk levels above 9 wrap back around to 1. So, if your original map had some
    position with a risk level of 8, then that same position on each of the 25 total tiles would be as follows:

    8 9 1 2 3
    9 1 2 3 4
    1 2 3 4 5
    2 3 4 5 6
    3 4 5 6 7
    """
    new_grid = [[0 for _ in range(5 * len(data[0]))] for __ in range(5 * len(data))]
    rows = len(data)
    columns = len(data[0])
    for row_expansion in range(5):
        for column_expansion in range(5):
            for row in range(len(data)):
                for col in range(len(data[0])):
                    current_value = data[row][col]
                    new_val = current_value - 1 + column_expansion + row_expansion
                    new_val = new_val % 9 + 1
                    new_grid[row_expansion * rows + row][
                        column_expansion * columns + col
                    ] = new_val
    return new_grid


def part2(data):
    """Solve part 2.

    The entire cave is actually five times larger in both dimensions than you thought; the area you originally scanned
    is just one tile in a 5x5 tile area that forms the full map. Your original map tile repeats to the right and
    downward; each time the tile repeats to the right or downward, all of its risk levels are 1 higher than the tile
    immediately up or left of it. However, risk levels above 9 wrap back around to 1. So, if your original map had some
    position with a risk level of 8, then that same position on each of the 25 total tiles would be as follows:

    8 9 1 2 3
    9 1 2 3 4
    1 2 3 4 5
    2 3 4 5 6
    3 4 5 6 7
    """
    data = expand_map(data)
    grid = Grid(matrix=data)
    start = grid.node(0, 0)
    end = grid.node(len(data) - 1, len(data[0]) - 1)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)
    print("operations:", runs, "path length:", len(path))
    # Ignore the first node because it's not entered
    total_risk = sum([data[coords[1]][coords[0]] for coords in path]) - data[0][0]
    # print(grid.grid_str(path=path, start=start, end=end))
    return total_risk


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
