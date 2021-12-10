"""AoC 8, 2021"""

# Standard library imports
import pathlib
import sys
from aocd import data, submit
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class DigitDisplay:
    """Class to represent a digital display.

    0:      1:      2:      3:      4:
    aaaa    ....    aaaa    aaaa    ....
    b    c  .    c  .    c  .    c  b    c
    b    c  .    c  .    c  .    c  b    c
    ....    ....    dddd    dddd    dddd
    e    f  .    f  e    .  .    f  .    f
    e    f  .    f  e    .  .    f  .    f
    gggg    ....    gggg    gggg    ....

    5:      6:      7:      8:      9:
    aaaa    aaaa    aaaa    aaaa    aaaa
    b    .  b    .  .    c  b    c  b    c
    b    .  b    .  .    c  b    c  b    c
    dddd    dddd    ....    dddd    dddd
    .    f  e    f  .    f  e    f  .    f
    .    f  e    f  .    f  e    f  .    f
    gggg    gggg    ....    gggg    gggg
    """

    digits: dict

    def __init__(self):
        self.digits = {}

    def add_digit(self, segments: str) -> None:
        sorted_segment = str(sorted(segments))
        if len(segments) == 2:
            self.digits[1] = set(segments)
            self.digits[sorted_segment] = 1
        elif len(segments) == 3:
            self.digits[7] = set(segments)
            self.digits[sorted_segment] = 7
        elif len(segments) == 4:
            self.digits[4] = set(segments)
            self.digits[sorted_segment] = 4
        elif len(segments) == 7:
            self.digits[8] = set(segments)
            self.digits[sorted_segment] = 8

    def decode_segment(self, segments: set) -> int:
        """Decode segment."""
        all_segments = self.digits[8]
        unknown_segments = set(segments)
        extra_segments = all_segments - unknown_segments
        ret = None
        if len(extra_segments) == 1:  # either a 0/6/9
            if len(extra_segments - self.digits[4]) == 1:  # must be a 9
                ret = 9
            elif len(extra_segments - self.digits[1]) == 0:  # must be a 6
                ret = 6
            else:  # must be a 0
                ret = 0
        elif len(extra_segments) == 2:  # either a 2/3/5
            if len(extra_segments - self.digits[1]) == 2:  # must be a 3
                ret = 3
            elif len(extra_segments - self.digits[4]) == 1:  # must be a 5
                ret = 5
            else:
                ret = 2
        return ret

    def convert_digit(self, segments: str) -> int:
        sorted_segment = str(sorted(segments))
        if sorted_segment in self.digits:
            return self.digits[sorted_segment]
        else:
            digit = self.decode_segment(set(segments))
            self.digits[sorted_segment] = digit
            self.digits[digit] = set(segments)
            return digit


def parse(puzzle_input):
    """Parse input"""
    output = []
    # This could be a list comprehension but :shrug:
    for entry in puzzle_input.splitlines():
        signal_pattern, output_value = entry.split("|")
        signal_pattern = signal_pattern.strip().split(" ")
        output_value = output_value.strip().split(" ")
        output.append((signal_pattern, output_value))
    return output


def part1(data):
    """Solve part 1.
    Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be able to tell which
    combinations of signals correspond to those digits. Counting only digits in the output values (the part after | on
    each line), in the above example, there are 26 instances of digits that use a unique number of segments (highlighted
    above).
    """
    total_unique_digits = 0
    for entry in data:
        signal_pattern, output_value = entry
        for digit in output_value:
            if len(digit) in (2, 3, 4, 7):
                total_unique_digits += 1
    return total_unique_digits


def part2(data):
    """Solve part 2"""
    total_digits = 0
    for entry in data:
        signal_pattern, output_value = entry
        decoder = DigitDisplay()
        for digit in signal_pattern:
            if len(digit) in (2, 3, 4, 7):
                decoder.add_digit(digit)
        for digit in output_value:
            if len(digit) in (2, 3, 4, 7):
                decoder.add_digit(digit)
        decoder_digits = ""
        for digit in output_value:
            decoder_digits += str(decoder.convert_digit(digit))
        total_digits += int(decoder_digits)
    return total_digits


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    answer_a, answer_b = solve(puzzle_input=data)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
