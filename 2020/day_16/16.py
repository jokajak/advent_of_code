#!/usr/bin/env python3

from collections import Counter
from math import prod
from re import match

import pytest
from parse import parse


class DoubleRange(object):
    def __init__(self, a, b, c, d):
        self.a, self.b, self.c, self.d = a, b, c, d

    def __contains__(self, value):
        return self.a <= value <= self.b or self.c <= value <= self.d


def parse_rules(inputs):
    """Extract rules from inputs

    Args:
        inputs (list): list of rules
    """
    rules = {}
    for line in inputs:
        rule = parse(
            "{field_name}: {min_val}-{low_range_upper} or {high_range_lower}-{max_val}",
            line,
        )
        if rule is not None:
            rules[rule["field_name"]] = (
                (int(rule["min_val"]), int(rule["low_range_upper"])),
                (int(rule["high_range_lower"]), int(rule["max_val"])),
            )
    return rules


class Ticket(object):
    def __init__(self, rules, fields):
        if rules is None:
            raise ValueError("Rules must be defined")
        self.rules = rules
        self.fields = list(map(int, fields.split(",")))

    def invalid_field(self):
        for value in self.fields:
            is_valid = False
            for _rule, values in self.rules.items():
                for range in values:
                    low, high = range
                    if low <= value <= high:
                        is_valid = True
            if not is_valid:
                return value
        return 0

    def field_name(self, value):
        rule_name = []
        for rule, values in self.rules.items():
            for range in values:
                low, high = range
                if low <= value <= high:
                    rule_name.append(rule)
        return rule_name

    def __str__(self):
        return ",".join(self.fields)


inputs = []
with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip("\n")
        inputs.append(line)

rules = parse_rules(inputs)
found_other_tickets = False
error_rate = 0
valid_tickets = []
for line in inputs:
    if line == "nearby tickets:":
        found_other_tickets = True
        continue
    if found_other_tickets:
        ticket = Ticket(rules, line)
        errors = ticket.invalid_field()
        error_rate += errors
        if errors == 0:
            valid_tickets.append(ticket)

print(error_rate)

my_ticket = False
for line in inputs:
    if line == "your ticket:":
        my_ticket = True
        continue
    if my_ticket is True:
        my_ticket = Ticket(rules, line)

n_fields = len(valid_tickets[0].fields)
possible = [set(range(n_fields)) for _ in range(len(rules))]
valid_tickets.append(my_ticket)
for ticket in valid_tickets:
    # For every field and its set of possible indexes
    for rng, poss in zip(rules, possible):
        # For each value in the ticket
        for i, value in enumerate(ticket.fields):
            # If that value cannot be valid for this field, then remove its
            # index from the possible indexes for the field
            is_possible = False
            for range in rules[rng]:
                low, high = range
                if low <= value <= high:
                    is_possible = True
            if not is_possible and i in poss:
                poss.remove(i)


for i, p in enumerate(possible):
    print(i, p)


def simplify(possible):
    # Start with None for all fields so that we can catch errors later if some None is not replaced.
    assigned = [None] * len(possible)

    # Continue until all sets of possible indexes are empty (i.e. we assigned each field an index)
    while any(possible):
        # For each set of possible indexes
        for i, poss in enumerate(possible):
            # If only one possible index is left, then it must be assigned to this field
            if len(poss) == 1:
                assigned[i] = match = poss.pop()
                break

        # Remove the assigned value from every other set
        for other in possible:
            if match in other:
                other.remove(match)

    # Optionally check for correctness
    #assert all(a is not None for a in assigned)

    return assigned


indexes = simplify(possible)[:6]

for i, p in enumerate(indexes):
    print(i, p)


total = prod(my_ticket.fields[i] for i in indexes if i is not None)
print('Part 2:', total)
