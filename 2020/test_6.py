#!/usr/bin/env python

# As your flight approaches the regional airport where you'll switch to a much larger plane, customs
# declaration forms are distributed to the passengers.
#
# The form asks a series of 26 yes-or-no questions marked a through z. All you need to do is identify the questions for
# which anyone in your group answers "yes". Since your group is just you, this doesn't take very long.
#
# However, the person sitting next to you seems to be experiencing a language barrier and asks if you can help. For each
# of the people in their group, you write down the questions for which they answer "yes", one per line. For example:
#
# abcx abcy abcz In this group, there are 6 questions to which anyone answered "yes": a, b, c, x, y, and z. (Duplicate
# answers to the same question don't count extra; each question counts at most once.)
#
# Another group asks for your help, then another, and eventually you've collected answers from every group on the plane
# (your puzzle input). Each group's answers are separated by a blank line, and within each group, each person's answers
# are on a single line. For example:
#
# abc
#
# a b c
#
# ab ac
#
# a a a a
#
# b
#
# This list represents answers from five groups:
#
# The first group contains one person who answered "yes" to 3 questions: a, b, and c. The second group contains three
# people; combined, they answered "yes" to 3 questions: a, b, and c. The third group contains two people; combined, they
# answered "yes" to 3 questions: a, b, and c. The fourth group contains four people; combined, they answered "yes" to
# only 1 question, a. The last group contains one person who answered "yes" to only 1 question, b. In this example, the
# sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.
#
# For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?

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
    # Part one
    input = []
    all_group_answers = []
    group_answers = set()
    for line in args.file.readlines():
        line = line.strip("\n")
        input.append(line)
        if line == "":
            # end of record
            all_group_answers.append(group_answers)
            group_answers = set()
        else:
            group_answers = group_answers.union(set(line))
    else:
        all_group_answers += group_answers

    total_yes_answers = 0
    for group in all_group_answers:
        total_yes_answers += len(group)

    print(total_yes_answers)

    # As you finish the last group's customs declaration, you notice that you misread one word in the instructions:
    #
    # You don't need to identify the questions to which anyone answered "yes"; you need to identify the questions to
    # which everyone answered "yes"!
    #
    # Using the same example as above:
    #
    # abc
    #
    # a
    # b
    # c
    #
    # ab
    # ac
    #
    # a
    # a
    # a
    # a
    #
    # b
    # This list represents answers from five groups:
    #
    # In the first group, everyone (all 1 person) answered "yes" to 3 questions: a, b, and c.
    # In the second group, there is no question to which everyone answered "yes".
    # In the third group, everyone answered yes to only 1 question, a. Since some people did not answer "yes" to b or c,
    # they don't count.
    # In the fourth group, everyone answered yes to only 1 question, a.
    # In the fifth group, everyone (all 1 person) answered "yes" to 1 question, b.
    # In this example, the sum of these counts is 3 + 0 + 1 + 1 + 1 = 6.
    #
    # For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?
    all_group_answers = []
    group_answers = None
    for line in input:
        if line == "":
            # end of record
            all_group_answers.append(group_answers)
            group_answers = None
            continue
        if group_answers is None:
            group_answers = set(line)
        else:
            group_answers = group_answers.intersection(set(line))
    else:
        if group_answers is not None:
            all_group_answers.append(group_answers)

    total_yes_answers = 0
    for group in all_group_answers:
        total_yes_answers += len(group)

    print(total_yes_answers)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("--file", type=argparse.FileType("r"), help="Input file", default="2020/inputs/6.test")

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
    ("abc", {"a", "b", "c"})
])
def test_split_range(input, expected):
    assert set(input) == expected
