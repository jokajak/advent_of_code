#!/usr/bin/env python
"""Solutions for AoC 8, 2022."""
# Created: 2022-12-08 08:44:55.159948

# Standard library imports
from aocd.models import Puzzle


def parse(input_data):
    """Transform the data"""
    ret = []
    for line in input_data.splitlines():
        row = []
        for character in line:
            row.append(int(character))
        ret.append(row)
    return ret


def expand_grid(grid):
    """Expand to add a row and column of zeros around the grid.

    This makes the calculation of visible easier."""

    # Start with a row of zeros
    # Add 2 columns to length of the row
    ret = [[-1] * (len(grid[-1]) + 2)]
    # Iterate through each row
    for row in grid:
        row.insert(0, -1)  # Add a zero to the beginning
        row.append(-1)  # add a zero at the end
        ret.append(row)
    ret.append([-1] * (len(grid) + 2))
    return ret


def position_is_visible(grid, row, column):
    """Calculate if a position is visible.

    Visible means the value is the max vertically or horizontally
    """

    def vertically_visible():
        ret = True
        for test_row in range(0, row):
            try:
                if grid[test_row][column] >= grid[row][column]:
                    ret = False
                    break
            except IndexError:
                print(f"{test_row} {column} {row} {len(grid[row])} {grid[row]}")
                raise
        else:
            return True
        for test_row in range(row + 1, len(grid)):
            if grid[test_row][column] >= grid[row][column]:
                ret = False
                break
        else:
            return True
        return ret

    def horizontally_visible():
        ret = True
        for test_col in range(0, column):
            # print(f"{grid[row][test_col]} >= {grid[row][column]}")
            if grid[row][test_col] >= grid[row][column]:
                ret = False
                break
        else:
            # print("Visible to the left")
            return True
        # print("Not visible to the left")
        for test_col in range(column + 1, len(grid[row])):
            if grid[row][test_col] >= grid[row][column]:
                ret = False
                break
        else:
            return True
        # print("Not visible to the right")
        return ret

    can_see_vertically = vertically_visible()
    can_see_horizontally = horizontally_visible()
    # print(f"Vertical: {can_see_vertically} Horizontal {can_see_horizontally}")
    # print(f"{grid[row]} {grid[row][column]}")
    return can_see_horizontally or can_see_vertically


def solve_part_one(input_data):
    """Solve part one.

        # --- Day 8: Treetop Tree House ---
    The expedition comes across a peculiar patch of tall trees all planted
     carefully in a grid. The Elves explain that a previous expedition
    planted these trees as a reforestation effort. Now, they're curious if
     this would be a good location for a [tree
    house](https://en.wikipedia.org/wiki/Tree_house).
    First, determine whether there is enough tree cover here to keep a
    tree house *hidden*. To do this, you need to count the number of trees
     that are *visible from outside the grid* when looking directly along
    a row or column.
    The Elves have already launched a
    [quadcopter](https://en.wikipedia.org/wiki/Quadcopter) to generate a
    map with the height of each tree (*your puzzle input*). For example:
    ```
    30373
    25512
    65332
    33549
    35390
    ```
    Each tree is represented as a single digit whose value is its height,
    where `0` is the shortest and `9` is the tallest.
    A tree is *visible* if all of the other trees between it and an edge
    of the grid are *shorter* than it. Only consider trees in the same row
     or column; that is, only look up, down, left, or right from any given
     tree.
    All of the trees around the edge of the grid are *visible* - since
    they are already on the edge, there are no trees to block the view. In
     this example, that only leaves the *interior nine trees* to consider:
     - The top-left `5` is *visible* from the left and top. (It isn't
    visible from the right or bottom since other trees of height `5` are
    in the way.)
     - The top-middle `5` is *visible* from the top and right.
     - The top-right `1` is not visible from any direction; for it to be
    visible, there would need to only be trees of height *0* between it
    and an edge.
     - The left-middle `5` is *visible*, but only from the right.
     - The center `3` is not visible from any direction; for it to be
    visible, there would need to be only trees of at most height `2`
    between it and an edge.
     - The right-middle `3` is *visible* from the right.
     - In the bottom row, the middle `5` is *visible*, but the `3` and `4`
     are not.
    With 16 trees visible on the edge and another 5 visible in the
    interior, a total of `21` trees are visible in this arrangement.
    Consider your map; *how many trees are visible from outside the grid?*
    """

    visible_nodes = []
    rows = len(input_data)
    columns = len(input_data[0])
    modified_grid = expand_grid(input_data)
    for row_index in range(1, rows + 1):
        for col in range(1, columns + 1):
            if position_is_visible(modified_grid, row_index, col):
                visible_nodes.append((row_index, col))
    answer = len(visible_nodes)
    return answer


def scenic_score(grid, row, column):
    """Calculate the scenic score for a position.

    To measure the viewing distance from a given tree, look up, down, left, and
    right from that tree; stop if you reach an edge or at the first tree that
    is the same height or taller than the tree under consideration. (If a tree
    is right on the edge, at least one of its viewing distances will be zero.)
    """

    tree_val = grid[row][column]
    print(tree_val)

    def vertical_score():
        score = 0
        for test_row in range(row - 1, 0, -1):
            print(f"grid[{test_row}][{column}] = {grid[test_row][column]}")
            if grid[test_row][column] < tree_val:
                if grid[test_row][column] == -1:
                    continue
                score += 1
            elif grid[test_row][column] >= tree_val:
                score += 1
                break
            else:
                break
        print(f"Up score {score}")
        total_score = score
        score = 0
        for test_row in range(row + 1, len(grid)):
            print(f"grid[{test_row}][{column}] = {grid[test_row][column]}")
            if grid[test_row][column] < tree_val:
                if grid[test_row][column] == -1:
                    continue
                score += 1
            elif grid[test_row][column] >= tree_val:
                score += 1
                break
            else:
                break
        total_score *= score
        print(f"Down score {score}")
        print(f"Vertical {total_score}")
        return total_score

    def horizontal_score():
        score = 0
        for test_col in range(column - 1, 0, -1):
            # print(f"{grid[row][test_col]} >= {grid[row][column]}")
            print(f"grid[{row}][{test_col}] = {grid[row][test_col]}")
            if grid[row][test_col] < grid[row][column]:
                if grid[row][test_col] == -1:
                    continue
                score += 1
            elif grid[row][test_col] >= grid[row][column]:
                score += 1
                break
            else:
                break
        print(f"Left score {score}")
        total_score = score
        score = 0
        for test_col in range(column + 1, len(grid[row])):
            print(f"grid[{row}][{test_col}] = {grid[row][test_col]}")
            if grid[row][test_col] < grid[row][column]:
                if grid[row][test_col] == -1:
                    continue
                score += 1
            elif grid[row][test_col] >= grid[row][column]:
                score += 1
                break
            else:
                break
        total_score *= score
        print(f"Right score {score}")
        print(f"Horizontal {total_score}")
        return total_score

    return vertical_score() * horizontal_score()


def solve_part_two(input_data):
    """Solve part two.

    Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

    To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

    The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

    In the example above, consider the middle 5 in the second row:

    30373
    25512
    65332
    33549
    35390

        Looking up, its view is not blocked; it can see 1 tree (of height 3).
        Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
        Looking right, its view is not blocked; it can see 2 trees.
        Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).

    A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

    However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

    30373
    25512
    65332
    33549
    35390

        Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
        Looking left, its view is not blocked; it can see 2 trees.
        Looking down, its view is also not blocked; it can see 1 tree.
        Looking right, its view is blocked at 2 trees (by a massive tree of height 9).

    This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

    Consider each tree on your map. What is the highest scenic score possible for any tree?

    """

    answer = None
    scenic_scores = []
    rows = len(input_data)
    columns = len(input_data[0])
    modified_grid = expand_grid(input_data)
    for row_index in range(1, rows + 1):
        for col in range(1, columns + 1):
            scenic_scores.append(scenic_score(modified_grid, row_index, col))
    print(scenic_scores)
    answer = max(scenic_scores)
    return answer


def main():
    puzzle = Puzzle(year=2022, day=8)
    parsed_data = parse(puzzle.input_data)
    answer_a = solve_part_one(parsed_data)
    if answer_a:
        puzzle.answer_a = answer_a
    parsed_data = parse(puzzle.input_data)
    answer_b = solve_part_two(parsed_data)
    if answer_b:
        puzzle.answer_b = answer_b


if __name__ == "__main__":
    main()
