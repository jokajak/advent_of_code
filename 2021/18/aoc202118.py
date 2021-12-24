"""AoC 18, 2021"""

# Standard library imports
import pathlib
import sys
from typing import Tuple
import math
import json
from dataclasses import dataclass
from aocd import data as input_data, submit


def str_to_list(num: str) -> list:
    ret = []
    current_number = ""
    for char in num:
        if char == "[":
            ret.append(char)
        elif char in ",]":
            if current_number != "":
                ret.append(int(current_number))
                current_number = ""
            if char == "]":
                ret.append(char)
        elif char in "0123456789":
            current_number += char
        else:
            raise ValueError("Unknown character")
    return ret


def explode_snailfish_number(num: list) -> Tuple[list, bool]:
    if isinstance(num, str):
        num = str_to_list(num)
    ret = []
    depth = 0
    pos = -1
    exploded = False
    while pos < len(num) - 1:
        pos += 1
        char = num[pos]
        if char == "[":
            depth += 1
            ret.append(char)
            continue
        elif char == "]":
            depth -= 1
            ret.append(char)
            continue
        elif exploded:
            ret.append(char)
            continue
        if depth > 4 and not exploded:
            # if we get here then we are on the left number of an exploding pair
            # look left for a number to add
            added = False
            exploded = True
            for new_char in range(pos - 1, 0, -1):
                if isinstance(ret[new_char], int):
                    ret[new_char] += char
                    break
            ret.pop()
            ret.append(0)
            # go past the left number
            pos += 1
            num_to_add = num[pos]
            # skip the right number
            pos += 1
            # skip the right bracket
            pos += 1
            # look right for a number to add
            for new_char in range(pos, len(num)):
                if isinstance(num[new_char], str):
                    ret.append(num[new_char])
                elif not added:  # number
                    ret.append(num[new_char] + num_to_add)
                    added = True
                else:
                    ret.append(num[new_char])
            break
        else:
            ret.append(char)
    return ret, exploded


def split_snailfish_number(num: list) -> list:
    """Split a snailfish number.

    To split a regular number, replace it with a pair; the left element of the pair should be the regular number divided
    by two and rounded down, while the right element of the pair should be the regular number divided by two and rounded
    up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
    """
    if isinstance(num, str):
        num = str_to_list(num)
    ret = []
    pos = 0
    split = False
    while pos < len(num):
        char = num[pos]
        pos += 1
        if isinstance(char, int) and char >= 10 and not split:
            left = math.floor(char / 2)
            right = math.ceil(char / 2)
            ret.append("[")
            ret.append(left)
            ret.append(right)
            ret.append("]")
            split = True
            continue
        ret.append(char)
    return ret, split


def list_to_str(num: list) -> str:
    ret = []
    for i in range(len(num) - 1):
        ret.append(str(num[i]))
        if isinstance(num[i], int):
            if isinstance(num[i + 1], int) or num[i + 1] == "[":
                ret.append(",")
            if num[i - 1] == "]":
                ret.pop()
                ret.append(",")
                ret.append(str(num[i]))
        if num[i] == "]" and num[i + 1] == "[":
            ret.append(",")
    ret.append(num[-1])
    return "".join(ret)


def calculate_magnitude(num: list) -> int:
    """Calculate magnitude of snailfish number.

    To check whether it's the right answer, the snailfish teacher only checks the magnitude of the final sum. The
    magnitude of a pair is 3 times the magnitude of its left element plus 2 times the magnitude of its right element.
    The magnitude of a regular number is just that number.

    Expects a list of ints or lists
    """
    if isinstance(num, int):
        return num
    return 3 * calculate_magnitude(num[0]) + 2 * calculate_magnitude(num[1])


@dataclass
class SnailfishNumber:
    num: list

    def __init__(self, num_in: str):
        self.num = str_to_list(num_in)

    def __str__(self) -> str:
        return list_to_str(self.num)

    @property
    def magnitude(self) -> int:
        num = json.loads(list_to_str(self.num))
        magnitude = calculate_magnitude(num)
        return magnitude

    def __add__(self, addend):
        num = list_to_str(self.num)
        addend = list_to_str(addend.num)
        ret = f"[{num},{addend}]"
        return SnailfishNumber(ret)

    def reduce(self):
        """Reduce a snailfish number.

        During reduction, at most one action applies, after which the process returns to the top of the list of actions.
        For example, if split produces a pair that meets the explode criteria, that pair explodes before other splits
        occur.
        """
        num = self.num
        while True:
            num, exploded = explode_snailfish_number(num)
            if exploded:
                continue
            num, split = split_snailfish_number(num)
            if split:
                continue
            break
        self.num = num


def parse(puzzle_input):
    """Parse input"""
    ret = []
    for line in puzzle_input.splitlines():
        ret.append(line)
    return ret


def part1(data):
    """Solve part 1"""
    num = SnailfishNumber(data[0])
    for line in data[1:]:
        num.reduce()
        num += SnailfishNumber(line)
    num.reduce()
    return num.magnitude


def part2(data):
    """Solve part 2.

    What is the largest magnitude of any sum of two different snailfish numbers from the homework assignment?"""
    max_magnitude = 0
    for entry in data:
        fish = SnailfishNumber(entry)
        for other_entry in data:
            new_fish = fish + SnailfishNumber(other_entry)
            new_fish.reduce()
            max_magnitude = max(new_fish.magnitude, max_magnitude)
    return max_magnitude



def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))

    answer_a, answer_b = solve(puzzle_input=input_data)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
