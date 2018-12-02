#!/usr/bin/env python3
"""
Advent of Code 2018, Day 2
"""

__author__ = "Josh"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse
import logging
import logzero
from collections import defaultdict
from logzero import logger


def main(args):
    """ Main entry point of the app """
    if (0 == args.verbose):
        logzero.loglevel(logging.INFO)
    elif (1 == args.verbose):
        logzero.loglevel(logging.DEBUG)
    two_char = 0
    three_char = 0
    for line in args.input.readlines():
        line = line.strip()
        histogram = defaultdict(int)
        for letter in line:
            histogram[letter] += 1
        logger.debug(histogram)
        inc_two = True
        inc_three = True
        for letter in histogram:
            if (2 == histogram[letter] and inc_two):
                two_char += 1
                inc_two = False
                logger.debug('Two: {}'.format(two_char))
            if (3 == histogram[letter] and inc_three):
                inc_three = False
                three_char += 1
    checksum = two_char * three_char
    msg = '{}, {}, {}'.format(two_char, three_char, checksum)
    logger.info(msg)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument(
        "input",
        type=argparse.FileType('r'),
        help="Required positional argument"
    )

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
