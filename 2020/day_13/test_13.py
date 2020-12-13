#!/usr/bin/env python


__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse

import pytest


def main(args):
    """Main program flow

    Args:
        args (argparse.Namespace): Parsed arguments
    """
    for line in args.file.readlines():
        line = line.strip("\n")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("--file", type=argparse.FileType("r"), help="Input file", default="2020/inputs/5")

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
def test_split_range(low, high, result_1, result_2):
    pass


@pytest.mark.parametrize("seat_id, expected", [
    ("FBFBBFFRLR", 357),
    ("BFFFBBFRRR", 567),
])
def test_BoardingPass(seat_id, expected):
    pass
