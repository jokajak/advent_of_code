#!/usr/bin/env python


__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse
from collections import Counter

import pytest


def count_neighbors(grid, row, column, immediate_neighbors):
    """Count the number of occupied neighbors

    Args:
        grid (list of lists): Current grid
        row (int): current row
        column (int): target column
    """
    # . == floor, never changes
    # # == occupied
    # L == empty
    occupied_neighbors = 0
    if immediate_neighbors:
        if row == 0:
            if grid[row+1][column] == "#":
                occupied_neighbors += 1
            if column == 0:
                if grid[row][column+1] == "#":
                    occupied_neighbors += 1
                if grid[row+1][column+1] == "#":
                    occupied_neighbors += 1
            elif column == len(grid[row])-1:
                if grid[row][column-1] == "#":
                    occupied_neighbors += 1
                if grid[row+1][column-1] == "#":
                    occupied_neighbors += 1
            else:
                if grid[row][column-1] == "#":
                    occupied_neighbors += 1
                if grid[row][column+1] == "#":
                    occupied_neighbors += 1
                if grid[row+1][column-1] == "#":
                    occupied_neighbors += 1
                if grid[row+1][column+1] == "#":
                    occupied_neighbors += 1
        elif row == len(grid)-1:
            if grid[row-1][column] == "#":
                occupied_neighbors += 1
            if column == 0:
                if grid[row][column+1] == "#":
                    occupied_neighbors += 1
                if grid[row-1][column+1] == "#":
                    occupied_neighbors += 1
            elif column == len(grid[row])-1:
                if grid[row][column-1] == "#":
                    occupied_neighbors += 1
                if grid[row-1][column-1] == "#":
                    occupied_neighbors += 1
            else:
                if grid[row][column-1] == "#":
                    occupied_neighbors += 1
                if grid[row][column+1] == "#":
                    occupied_neighbors += 1
                if grid[row-1][column-1] == "#":
                    occupied_neighbors += 1
                if grid[row-1][column+1] == "#":
                    occupied_neighbors += 1
        else:
            if grid[row+1][column] == "#":
                occupied_neighbors += 1
            if grid[row-1][column] == "#":
                occupied_neighbors += 1
            if column == 0:
                if grid[row+1][column+1] == "#":
                    occupied_neighbors += 1
                if grid[row][column+1] == "#":
                    occupied_neighbors += 1
                if grid[row-1][column+1] == "#":
                    occupied_neighbors += 1
            elif column == len(grid[row])-1:
                if grid[row+1][column-1] == "#":
                    occupied_neighbors += 1
                if grid[row][column-1] == "#":
                    occupied_neighbors += 1
                if grid[row-1][column-1] == "#":
                    occupied_neighbors += 1
            else:
                if grid[row+1][column-1] == "#":
                    occupied_neighbors += 1
                if grid[row+1][column+1] == "#":
                    occupied_neighbors += 1
                if grid[row][column-1] == "#":
                    occupied_neighbors += 1
                if grid[row][column+1] == "#":
                    occupied_neighbors += 1
                if grid[row-1][column-1] == "#":
                    occupied_neighbors += 1
                if grid[row-1][column+1] == "#":
                    occupied_neighbors += 1
    else:
        current_col = [r[row][column] for r in grid]
        if row == 0:
            # look down
            remaining_spots = "".join(current_col[row+1:]).strip(".")
            if remaining_spots[0] == "#":
                occupied_neighbors += 1
            if column == 0:
                # look right
                remaining_spots = "".join(grid[row][column+1:]).strip(".")
                if remaining_spots[0] == "#":
                    occupied_neighbors += 1
            elif column == len(grid[row])-1:
                # look left
                remaining_spots = "".join(grid[row][:column-1]).strip(".")
                if remaining_spots[-1] == "#":
                    occupied_neighbors += 1
            else:
                # look right
                remaining_spots = "".join(grid[row][column+1:]).strip(".")
                if remaining_spots[0] == "#":
                    occupied_neighbors += 1
                # look left
                remaining_spots = "".join(grid[row][:column-1]).strip(".")
                if remaining_spots[-1] == "#":
                    occupied_neighbors += 1
        elif row == len(grid)-1:
            # look up
            remaining_spots = "".join(current_col[:row-1]).strip(".")
            if remaining_spots[-1] == "#":
                occupied_neighbors += 1
            if column == 0:
                # look right
                remaining_spots = "".join(grid[row][column+1:]).strip(".")
                if remaining_spots[0] == "#":
                    occupied_neighbors += 1
            elif column == len(grid[row])-1:
                # look left
                remaining_spots = "".join(grid[row][:column-1]).strip(".")
                if remaining_spots[-1] == "#":
                    occupied_neighbors += 1
            else:
                # look right
                remaining_spots = "".join(grid[row][column+1:]).strip(".")
                if remaining_spots[0] == "#":
                    occupied_neighbors += 1
                # look left
                remaining_spots = "".join(grid[row][:column-1]).strip(".")
                if remaining_spots[-1] == "#":
                    occupied_neighbors += 1
        else:
            # look down
            remaining_spots = "".join(current_col[row+1:]).strip(".")
            if remaining_spots[0] == "#":
                occupied_neighbors += 1
            # look up
            remaining_spots = "".join(current_col[:row-1]).strip(".")
            if remaining_spots[-1] == "#":
                occupied_neighbors += 1
            if column == 0:
                # look right
                remaining_spots = "".join(grid[row][column+1:]).strip(".")
                if remaining_spots[0] == "#":
                    occupied_neighbors += 1
            elif column == len(grid[row])-1:
                # look left
                remaining_spots = "".join(grid[row][:column-1]).strip(".")
                if remaining_spots[-1] == "#":
                    occupied_neighbors += 1
            else:
                # look right
                remaining_spots = "".join(grid[row][column+1:]).strip(".")
                if remaining_spots[0] == "#":
                    occupied_neighbors += 1
                # look left
                remaining_spots = "".join(grid[row][:column-1]).strip(".")
                if remaining_spots[-1] == "#":
                    occupied_neighbors += 1
    return occupied_neighbors


def evolve_grid(grid, max_neighbors=4, immediate_neighbors=True):
    """Evolve a grid

    Args:
        grid (list of lists): Grid contents
        max_neighbors (int): max neighbors to flip
        immediate_neighbors (boolean): Whether or not immediate neighbors are counted
    """
    new_grid = []
    # . == floor, never changes
    # # == occupied
    # L == empty
    for row in range(len(grid)):
        new_row = []
        for column in range(len(grid[row])):
            occupied_neighbors = count_neighbors(grid, row, column, immediate_neighbors)
            spot = grid[row][column]
            if spot == ".":
                new_row.append(".")
                continue  # floors never change
            elif spot == "L":
                if occupied_neighbors == 0:
                    new_row.append("#")
                else:
                    new_row.append("L")
            elif spot == "#":
                if occupied_neighbors >= max_neighbors:
                    new_row.append("L")
                else:
                    new_row.append("#")
        new_grid.append(new_row)
    return new_grid


def main(args):
    """Main program flow

    Args:
        args (argparse.Namespace): Parsed arguments
    """
    rows = []
    for line in args.file.readlines():
        line = line.strip("\n")
        row = list(line)
        rows.append(row)
    current_grid = rows
    seen_grids = set()
    max_attempts = 100
    for _attempt in range(max_attempts):
        next_grid = evolve_grid(current_grid)
        if str(next_grid) in seen_grids:
            break
        current_grid = next_grid
        print(_attempt)
    occupied = Counter()
    for row in current_grid:
        occupied.update("".join(row))
        print(''.join(row))
    print(occupied["#"])


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("--file", type=argparse.FileType("r"), help="Input file", default="2020/inputs/day_11/test.txt")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)


# TESTS

@pytest.mark.parametrize("input, expected", [
])
def test_split_range(input, expected):
    assert input == expected
