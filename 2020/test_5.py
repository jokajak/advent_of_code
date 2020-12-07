#!/usr/bin/env python

__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse

import pytest


def split_range(low, high):
    """Split a range

    Args:
        low (int): Low number
        high (int): High number
    """
    num_range = (high - low) + 1
    mid = high - (num_range / 2)
    return (low, mid), ((mid + 1), high)


class BoardingPass(object):
    def __init__(self, enc_seat_id):
        self.row_num = BoardingPass.get_row_from_id(enc_seat_id)
        self.seat_num = BoardingPass.get_seat_from_id(enc_seat_id)
        self.seat_id = self.row_num * 8 + self.seat_num
        self.enc_seat_id = enc_seat_id

    @staticmethod
    def get_row_from_id(seat_id):
        low_row_num = 0
        high_row_num = 127
        for char in seat_id:
            low_range, high_range = split_range(low_row_num, high_row_num)
            if char == "F":
                low_row_num, high_row_num = low_range
            elif char == "B":
                low_row_num, high_row_num = high_range
        if low_row_num != high_row_num:
            raise ValueError("Invalid seat id")
        else:
            return low_row_num

    @staticmethod
    def get_seat_from_id(seat_id):
        low_seat_num = 0
        high_seat_num = 7
        for char in seat_id:
            low_range, high_range = split_range(low_seat_num, high_seat_num)
            if char == "L":
                low_seat_num, high_seat_num = low_range
            elif char == "R":
                low_seat_num, high_seat_num = high_range
        if low_seat_num != high_seat_num:
            raise ValueError("Invalid seat id")
        else:
            return low_seat_num


def main(args):
    """Main program flow

    Args:
        args (argparse.Namespace): Parsed arguments
    """
    max_seat_id = 0
    all_seat_ids = []
    for line in args.file.readlines():
        line = line.strip("\n")
        try:
            boarding_pass = BoardingPass(line)
        except ValueError:
            continue
        if boarding_pass.seat_id > max_seat_id:
            max_seat_id = boarding_pass.seat_id
        all_seat_ids.append(boarding_pass.seat_id)

    print(max_seat_id)
    sorted_seat_ids = sorted(all_seat_ids)
    for index, seat_id in enumerate(sorted_seat_ids):
        if sorted_seat_ids[index+1] != seat_id + 1:
            print(seat_id + 1)
            break

    print(sorted_seat_ids)


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

@pytest.mark.parametrize("low,high,result_1,result_2", [
    (0, 127, (0, 63), (64, 127)),
    (0, 63, (0, 31), (32, 63)),
    (32, 63, (32, 47), (48, 63)),
    (32, 47, (32, 39), (40, 47)),
    (40, 47, (40, 43), (44, 47)),
    (44, 47, (44, 45), (46, 47)),
    (44, 45, (44, 44), (45, 45)),
    (0, 7, (0, 3), (4, 7)),
    (4, 7, (4, 5), (6, 7)),
    (4, 5, (4, 4), (5, 5)),
])
def test_split_range(low, high, result_1, result_2):
    assert split_range(low, high) == (result_1, result_2)


@pytest.mark.parametrize("seat_id, expected", [
    ("FBFBBFFRLR", 357),
    ("BFFFBBFRRR", 567),
])
def test_BoardingPass(seat_id, expected):
    boarding_pass = BoardingPass(seat_id)
    assert boarding_pass.seat_id == expected

# Start by considering the whole range, rows 0 through 127.
# F means to take the lower half, keeping rows 0 through 63.
# B means to take the upper half, keeping rows 32 through 63.
# F means to take the lower half, keeping rows 32 through 47.
# B means to take the upper half, keeping rows 40 through 47.
# B keeps rows 44 through 47.
# F keeps rows 44 through 45.
# The final F keeps the lower of the two, row 44.
#

# Start by considering the whole range, columns 0 through 7.
# R means to take the upper half, keeping columns 4 through 7.
# L means to take the lower half, keeping columns 4 through 5.
# The final R keeps the upper of the two, column 5.
