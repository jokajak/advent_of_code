#!/usr/bin/env python3
"""
Advent of Code 2018, Day 5
"""

__author__ = "Josh"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse
import logging
import logzero
from collections import defaultdict
from logzero import logger


def purge_pairs(in_str):
    i = 1
    out_str = ''
    while i < len(in_str):
        if not ((in_str[i].lower() == in_str[i-1].lower()) and
                (in_str[i] != in_str[i-1])):
            out_str += in_str[i-1]
            i += 1
        else:
            logger.debug('Paired {}{}'.format(in_str[i-1], in_str[i]))
            i += 2
    if i == len(in_str):
        out_str += in_str[i-1]
    logger.debug('{} {}'.format(in_str, out_str))
    return in_str, out_str


def main(args):
    """ Main entry point of the app """
    if (0 == args.verbose):
        logzero.loglevel(logging.INFO)
    elif (1 == args.verbose):
        logzero.loglevel(logging.DEBUG)
    entries = []

    for line in args.input.readlines():
        line = line.strip()
        next_line = ''
        i = 0
        while i < len(line):
            line, next_line = purge_pairs(line)
            logger.debug(next_line)
            i += 1
            if line == next_line:
                break
            line = next_line
    logger.debug(next_line)
    logger.info(len(next_line))


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
