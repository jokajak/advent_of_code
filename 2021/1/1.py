#!/usr/bin/env python

__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse
from itertools import combinations


def main(args):
    """Main program flow

    Args:
        args (argparse.Namespace): Parsed arguments
    """
    entries = []

    for line in args.file.readlines():
        entries.append(int(line))

    previous_line = 0
    # Start at -1 so that the first line doesn't count
    number_increased = -1
    for line in entries:
        # print("%d + %d = %d" % (num_one, num_two, num_one + num_two))
        if line > previous_line:
            number_increased += 1
        previous_line = line

    print(f"Part one: {number_increased} depths increased")

    index = 3
    last_depth = 0
    # Start at -1 so that the first line doesn't count
    number_increased = 0
    while index < len(entries):
        current_depth = sum(entries[index - 3 : index])
        if current_depth > last_depth:
            number_increased += 1
        last_depth = current_depth
        index += 1

    print(f"Part two: {number_increased} depths increased")


if __name__ == "__main__":
    """This is executed when run from the command line"""
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("file", type=argparse.FileType("r"), help="Input file")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)
