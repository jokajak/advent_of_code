#!/usr/bin/env python3
"""
Advent of Code 2018 Day 1, part 1
"""

__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse


def main(args):
    """ Main entry point of the app """
    ret = 0
    for line in args.file.readlines():
        line = line.strip()
        action = line[0]
        if ('+' == action):
            ret += int(line[1:])
        elif ('-' == action):
            ret -= int(line[1:])
        else:
            print("Invalid input: {}".format(line))
    print(ret)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("file", type=argparse.FileType('r'), help="Input file")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
