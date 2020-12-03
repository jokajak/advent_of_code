#!/usr/bin/env python

__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse


def count_trees(tree_map, horizontal_moves, vertical_moves):
    """Count trees in a map

    Args:
        tree_map (dictionary): map of trees
        horizontal_moves (int): number of horizontal movements
        vertical_moves (int): number of vertical movements
    """
    total_trees = 0
    current_pos = 0
    # # right 3, down 1
    for current_row in tree_map:
        if current_row % vertical_moves == 0:
            total_trees += tree_map[current_row][current_pos % len(tree_map[current_row])]
            current_pos += horizontal_moves

    return total_trees


def main(args):
    """Main program flow

    Args:
        args (argparse.Namespace): Parsed arguments
    """
    tree_map = {}

    current_row = 0
    for line in args.file.readlines():
        tree_map_row = []
        tree_map[current_row] = tree_map_row
        current_row += 1
        for pos in line:
            if pos == ".":
                tree_map_row.append(0)
            elif pos == "#":
                tree_map_row.append(1)

    print(count_trees(tree_map, 3, 1))

    routes = (
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    )

    total_trees = 1
    for horizontal_moves, vertical_moves in routes:
        tree_count = count_trees(tree_map, horizontal_moves, vertical_moves)
        print(tree_count)
        total_trees *= tree_count

    print(total_trees)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("--file", type=argparse.FileType("r"), help="Input file", default="2020/input.3")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)
