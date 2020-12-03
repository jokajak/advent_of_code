#!/usr/bin/env python

__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse


def is_valid_password(policy, candidate_password):
    """Determine if provided password is valid."""
    char_range, test_char = policy.split(" ")
    min_count, max_count = char_range.split("-")
    char_count = candidate_password.count(test_char)
    if int(min_count) <= char_count and char_count <= int(max_count):
        return True
    return False


def is_valid_toboggan_password(policy, candidate_password):
    """Determine if provided password is valid toboggan password."""
    char_range, test_char = policy.split(" ")
    char_pos_one, char_pos_two = char_range.split("-")
    ret = False
    if (
        candidate_password[int(char_pos_one)-1] == test_char
        and candidate_password[int(char_pos_two)-1] == test_char
    ):
        ret = False
    elif (
        candidate_password[int(char_pos_one)-1] == test_char
        or candidate_password[int(char_pos_two)-1] == test_char
    ):
        ret = True
    print(ret, char_pos_one, char_pos_two, test_char, candidate_password)
    print(candidate_password[int(char_pos_one)-1], candidate_password[int(char_pos_two)-1])
    return ret


def main(args):
    """Main program flow

    Args:
        args (argparse.Namespace): Parsed arguments
    """
    entries = []

    for line in args.file.readlines():
        policy, candidate_password = line.split(":")
        candidate_password = candidate_password.strip('\n')
        entries.append((policy, candidate_password))

    valid_passwords = [
        candidate_password
        for policy, candidate_password in entries
        if is_valid_password(policy, candidate_password)
    ]

    print(len(valid_passwords))

    valid_passwords = [
        candidate_password
        for policy, candidate_password in entries
        if is_valid_toboggan_password(policy, candidate_password.strip(" "))
    ]

    print(len(valid_passwords))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("--file", type=argparse.FileType("r"), help="Input file", default="2020/input.2")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)
