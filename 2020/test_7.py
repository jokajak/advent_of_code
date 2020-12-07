#!/usr/bin/env python

# You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab
# some food: all flights are currently delayed due to issues in luggage processing.
#
# Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents;
# bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody
# responsible for these regulations considered how long they would take to enforce!
#
# For example, consider the following rules:
#
# light red bags contain 1 bright white bag, 2 muted yellow bags.
# dark orange bags contain 3 bright white bags, 4 muted yellow bags.
# bright white bags contain 1 shiny gold bag.
# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.
#
# These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every
# vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.
#
# You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be
# valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)
#
# In the above rules, the following options would be available to you:
#
# A bright white bag, which can hold your shiny gold bag directly.
# A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
# A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
# A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
# So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.
#
# How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure
# you get all of it.)


__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse
import re
from functools import lru_cache

import pytest


bag_rules = {}


@lru_cache
def holds_shiny_gold(bag_type):
    """Return a boolean if the bag can hold a shiny bag

    Args:
        rules (dictionary): dictionary of bag rules
        bag_type (string): Type of bag
    """
    ret = False
    if "shiny gold" in bag_rules[bag_type]:
        ret = True
    else:
        for bag in bag_rules[bag_type]:
            if not ret:
                ret = holds_shiny_gold(bag)
            if ret:
                break
    return ret


def parse_rule(rule):
    """Parse a rule

    Args:
        rule (string): The rule string
    Returns:
        parsed_rule (dict): A dictionary with a single key. The value for the key is a dictionary of colors as key and
        value as the number of bags

    light red bags contain 1 bright white bag, 2 muted yellow bags.
    {
        "light red bag": {
            "bright white bag": 1,
            "muted yellow bag": 2
        }
    }
    """

    regex = r"^(?P<outside_bag>.+) bags? contain (?P<inside_bags>.+)$"

    match = re.match(regex, rule)
    try:
        outside_bag, inside_bags = match.group("outside_bag"), match.group("inside_bags")
    except AttributeError:
        return {}

    parsed_rule = {outside_bag: {}}

    if inside_bags == "no other bags.":
        return parsed_rule
    regex = r"(?P<count>\d) (?P<bag>\S+\s\S+) bags?"

    matches = re.finditer(regex, inside_bags, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        bag_count = match.group('count')
        bag_type = match.group('bag')
        parsed_rule[outside_bag][bag_type] = int(bag_count)

    return parsed_rule


@lru_cache
def bags_held(bag_type):
    """Count the number of bags within a bag type

    Args:
        bag_type (string): The type of bag to count the contents
    """
    rules = bag_rules
    total_bags_held = 1
    for entry in rules[bag_type]:
        number_held = rules[bag_type][entry]
        total_bags_held += number_held * bags_held(entry)
    return total_bags_held


def main(args):
    """Main program flow

    Args:
        args (argparse.Namespace): Parsed arguments
    """
    for line in args.file.readlines():
        line = line.strip("\n")
        bag_rules.update(parse_rule(line))

    bags_that_hold_shiny_gold_bag = 0
    for bag_type in bag_rules:
        if holds_shiny_gold(bag_type=bag_type):
            bags_that_hold_shiny_gold_bag += 1

    print(bags_that_hold_shiny_gold_bag)

    # It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous
    # number of bags you need to buy!
    #
    # Consider again your shiny gold bag and the rules from the above example:
    #
    # faded blue bags contain 0 other bags.
    # dotted black bags contain 0 other bags.
    # vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
    # dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
    #
    # So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and
    # the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!
    #
    # Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count
    # all of the bags, even if the nesting becomes topologically impractical!
    #
    # Here's another example:
    #
    # shiny gold bags contain 2 dark red bags.
    # dark red bags contain 2 dark orange bags.
    # dark orange bags contain 2 dark yellow bags.
    # dark yellow bags contain 2 dark green bags.
    # dark green bags contain 2 dark blue bags.
    # dark blue bags contain 2 dark violet bags.
    # dark violet bags contain no other bags.
    #
    # In this example, a single shiny gold bag must contain 126 other bags.
    #
    # How many individual bags are required inside your single shiny gold bag?
    # Don't count the outermost bag
    print(bags_held("shiny gold") - 1)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument(
        "--file",
        type=argparse.FileType("r"),
        help="Input file",
        default="2020/inputs/7.test",
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)


# TESTS

# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
@pytest.mark.parametrize(
    "rule, expected",
    [
        (
            "light red bags contain 1 bright white bag, 2 muted yellow bags.",
            {
                "light red": {
                    "bright white": 1,
                    "muted yellow": 2,
                }
            },
        ),
        (
            "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
            {
                "dark orange": {
                    "bright white": 3,
                    "muted yellow": 4,
                }
            },
        ),
        (
            "bright white bags contain 1 shiny gold bag.",
            {
                "bright white": {
                    "shiny gold": 1,
                }
            },
        ),
        ("dotted black bags contain no other bags.", {"dotted black": {}}),
    ],
)
def test_split_range(rule, expected):
    assert parse_rule(rule) == expected
