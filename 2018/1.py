#!/usr/bin/env python3
"""
Advent of Code 2018 Day 1, part 1 and 2
"""

__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse


class Destination:
    frequency = 0
    freq_frequency = {}

    def change(self, delta):
        self.frequency += delta
        if (self.frequency in self.freq_frequency):
            self.freq_frequency[self.frequency] += 1
        else:
            self.freq_frequency[self.frequency] = 1

    def init(self):
        self.freq_frequency[self.frequency] = 1


def main(args):
    """ Main entry point of the app """
    my_dest = Destination()
    ret = 0
    loop_count = 1
    line_count = 1
    entries = []
    for line in args.file.readlines():
        line_count += 1
        line = line.strip()
        action = line[0]
        if ('+' == action):
            delta = int(line[1:])
        elif ('-' == action):
            delta = -1 * int(line[1:])
        else:
            print("Invalid input: {}".format(line))
        entries.append(delta)
        my_dest.change(delta)
    print(my_dest.frequency)
    while loop_count < 1000:
        loop_count += 1
        for entry in entries:
            line_count += 1
            my_dest.change(entry)
            if (my_dest.freq_frequency[my_dest.frequency] > 1):
                break
        else:
            continue
        break
    #print(loop_count, line_count, my_dest.frequency, my_dest.freq_frequency)
    print(my_dest.frequency, my_dest.freq_frequency[my_dest.frequency])


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
