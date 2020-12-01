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

    for num_one, num_two in combinations(entries, 2):
        # print("%d + %d = %d" % (num_one, num_two, num_one + num_two))
        if num_one + num_two == 2020:
            print(num_one * num_two)
    for numbers in combinations(entries, 3):
        # print("%d + %d = %d" % (num_one, num_two, num_one + num_two))
        a, b, c = numbers
        if a + b + c == 2020:
            print(a * b * c)


if __name__ == "__main__":
    """ This is executed when run from the command line """
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
