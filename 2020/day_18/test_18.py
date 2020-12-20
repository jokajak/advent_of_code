#!/usr/bin/env python

import pytest

OPERANDS = ("+", "*")


def prioritize_addition(expression):
    ret = 1
    operation = "*"
    mult_expression = []
    for val in expression:
        if val == "+":
            operation = val
        elif val == "*":
            operation = val
        elif operation == "+":
            lhs = int(mult_expression.pop())
            new_val = int(val) + int(lhs)
            mult_expression.append(new_val)
        elif operation == "*":
            mult_expression.append(val)

    for val in mult_expression:
        ret *= int(val)
    return ret


def compute_simple_expression(expression):
    ret = None
    operation = None
    for val in expression:
        if val in OPERANDS:
            operation = val
            continue
        if operation is not None:
            if operation == "*":
                ret *= int(val)
            elif operation == "+":
                ret += int(val)
            operation = None
        if ret is None:
            ret = int(val)
    return ret


def solve_expression(expression, advanced=False):
    # if "(" is in expression we need to recalculate
    # the expression to remove ()
    # walk through the expression to find the first (
    # walk backwards through the expression to find the first )
    # replace elements with value of solve_expression
    # pass resultant string to compute_simple_expression
    start_parens = []
    end_parens = []
    expression = prepare_expression(expression)
    for index, val in enumerate(expression):
        if "(" in val:
            start_parens.append(index)
        elif ")" in val:
            start = start_parens.pop()
            end = index
            new_entry = str(solve_expression(expression[start+1:end], advanced))
            expression[start:end+1] = [new_entry]
            return solve_expression(expression, advanced)

    if len(start_parens) == 0:
        if advanced:
            return prioritize_addition(expression)
        else:
            return compute_simple_expression(expression)
    else:
        # oh snap, sublist slicing:
        # https://stackoverflow.com/a/12898180
        raise ValueError


def prepare_expression(expression):
    for index, val in enumerate(expression):
        if "(" in val and val != "(":
            new_val = val.split("(")
            for i, result in enumerate(new_val):
                if result == "":
                    new_val[i] = "("
            expression[index:index+1] = new_val
            return prepare_expression(expression)
        if ")" in val and val != ")":
            new_val = val.split(")")
            for i, result in enumerate(new_val):
                if result == "":
                    new_val[i] = ")"
            expression[index:index+1] = new_val
            return prepare_expression(expression)
    return expression


@pytest.mark.parametrize(
    "input, expected",
    [
        ("1 + 2 * 3 + 4 * 5 + 6", 71),
        ("5 * 5 + 3 + 2", 30),
    ],
)
def test_compute_simple_expression(input, expected):
    assert compute_simple_expression(input.split(" ")) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("1 + 2 * 3 + 4 * 5 + 6", 71),
        ("1 + (2 * 3) + (4 * (5 + 6))", 51),
        ("2 * 3 + (4 * 5)", 26),
    ],
)
def test_solve_expression(input, expected):
    assert solve_expression(input.split(" ")) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (["(2", "+", "(2", "*", "3))"], ["(", "2", "+", "(", "2", "*", "3", ")", ")"]),
        (["(2", "*", "3)"], ["(", "2", "*", "3", ")"]),
    ],
)
def test_prepare_expression(input, expected):
    assert prepare_expression(input) == expected


def main():
    res = 0
    with open("input.txt") as f:
        for line in f.readlines():
            line = line.strip("\n")
            res += solve_expression(line.split(" "))

    print("Part 1: {}".format(res))

    res = 0
    with open("input.txt") as f:
        for line in f.readlines():
            line = line.strip("\n")
            res += solve_expression(line.split(" "), advanced=True)
    print("Part 2: {}".format(res))


if __name__ == "__main__":
    main()


@pytest.mark.parametrize(
    "input, expected",
    [
        ("5 * 5 + 3 + 2", 50),
    ],
)
def test_prioritize_addition(input, expected):
    assert prioritize_addition(input.split(" ")) == expected
