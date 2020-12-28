#!/usr/bin/env python

from collections import defaultdict

import pytest
from parse import parse


def parse_rules(inputs):
    rules = {}
    for line in inputs:
        rule = parse(
            "{rule_number}: {rule_value}",
            line,
        )
        if rule is not None:
            rule_options = rule["rule_value"].split(" | ")
            rule_choices = []
            if len(rule_options) == 1:
                rule_choices = rule["rule_value"].split(" ")
                if len(rule_choices) == 1:
                    rule_choices = rule["rule_value"].strip('"')
            else:
                for rule_option in rule_options:
                    option_parts = rule_option.split(" ")
                    rule_choices.append(option_parts)
            rules[rule["rule_number"]] = rule_choices
    return rules


def concat_rules(rules, rule):
    ret = []
    if len(rule) == 1:
        return resolve_rule(rules, rule[0])
    first_part = resolve_rule(rules, rule[0])
    second_part = resolve_rule(rules, rule[1])
    if isinstance(first_part, list):
        for entry in first_part:
            for e in second_part:
                new_entry = "{}{}".format(entry, e)
                ret.append(new_entry)
    else:
        if isinstance(second_part, list):
            for entry in second_part:
                new_entry = "{}{}".format(first_part, entry)
                ret.append(new_entry)
        else:
            ret.append("{}{}".format(first_part, second_part))
    return ret


def resolve_rule(rules, index):
    ret = []
    # Get rule entry
    rule = rules[index]
    # for entries of 1 2 | 2 1
    if isinstance(rule[0], list):
        for rule_set in rule:
            ret.extend(concat_rules(rules, rule_set))
    # covers entry of 1 2
    elif rule[0] in rules:
        ret.extend(concat_rules(rules, rule))
    # example entry: a
    else:
        ret = rule[0]
    return ret


def parse_input(fin):
    rules = {}

    for line in map(str.rstrip, fin):
        if not line:
            break

        rule_id, options = line.split(': ')
        rule_id = int(rule_id)

        if '"' in options:
            rule = options[1:-1]
        else:
            rule = []
            for option in options.split('|'):
                rule.append(tuple(map(int, option.split())))

        rules[rule_id] = rule

    return rules


def match(rules, string, rule=0, index=0):
    # If we are past the end of the string, we can't match anything anymore
    if index >= len(string):
        return []

    # Get the parsed rule for the current rule number
    rule = rules[rule]
    # If the current rule is a simple character, match that literally
    if type(rule) is str:
        # If it matches, advance 1 and return this information to the caller
        if string[index] == rule:
            return [index + 1]
        # Otherwise fail, we cannot continue matching
        return []

    # If we get here, we are in the case `X: A B | C D`
    matches = []

    # For each option
    for option in rule:
        # Start matching from the current position
        sub_matches = [index]

        # For any rule of this option
        for sub_rule in option:
            # Get all resulting positions after matching this rule from any of the
            # possible positions we have so far.
            new_matches = []
            for idx in sub_matches:
                new_matches += match(rules, string, sub_rule, idx)

            # Keep the new positions and continue with the next rule, trying to match all of them
            sub_matches = new_matches

        # Collect all possible matches for the current option and add them to the final result
        matches += sub_matches

    # Return all possible final indexes after matching this rule
    return matches


@pytest.mark.parametrize(
    "input, expected",
    [
        ([
            '0: 1 2',
            '1: "a"',
            '2: 1 3 | 3 1',
            '3: "b"',
        ], {
            "0": ["1", "2"],
            "1": ["a"],
            "2": [["1", "3"], ["3", "1"]],
            "3": ["b"],
        }
        ),
    ],
)
def test_parse_rules(input, expected):
    assert parse_rules(input) == expected


@pytest.mark.parametrize(
    "rules, input, expected",
    [
        (
            {
                "0": ["1", "2"],
                "1": ["a"],
                "2": [["1", "3"], ["3", "1"]],
                "3": ["b"],
            },
            "3",
            "b",
        ),
        (
            {
                "0": ["1", "3"],
                "1": ["a"],
                "2": [["1", "3"], ["3", "1"]],
                "3": ["b"],
            },
            "1",
            "a",
        ),
        (
            {
                "0": ["1", "2"],
                "1": ["a"],
                "2": [["1", "3"], ["3", "1"]],
                "3": ["b"],
            },
            "0",
            ["aab", "aba"],
        ),
    ],
)
def test_resolve_rule(rules, input, expected):
    assert resolve_rule(rules, input) == expected


def main():
    lines = []
    rules = []
    with open("input.txt") as f:
        for line in f.readlines():
            line = line.strip("\n")
            lines.append(line)

    rules = parse_rules(lines)

    valid_entries = set(resolve_rule(rules, "0"))

    part_one = 0
    for entry in lines:
        part_one += entry in valid_entries
    print("Part 1: ", part_one)

    rules = parse_input(lines)
    rules[8] = [(42,), (42, 8)]
    rules[11] = [(42, 31), (42, 11, 31)]
    valid2 = 0

    for entry in lines:
        if len(entry) in match(rules, entry):
            valid2 += 1

    # valid_entries = set(resolve_rule(rules, "0"))

    # part_two = 0
    # for entry in lines:
    #     part_two += entry in valid_entries
    print("Part 2: ", valid2)


if __name__ == "__main__":
    main()
