#!/usr/bin/env python

from collections import defaultdict

import pytest
from parse import parse

#materialized_rules = defaultdict([])


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
                    rule_choices = [rule["rule_value"].strip('"')]
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

    rules["8"] = [["42"], ["42", "8"]]
    rules["11"] = [["42", "31"], ["42", "11", "31"]]

    valid_entries = set(resolve_rule(rules, "0"))

    part_two = 0
    for entry in lines:
        part_two += entry in valid_entries
    print("Part 2: {}".format(part_two))


if __name__ == "__main__":
    main()
