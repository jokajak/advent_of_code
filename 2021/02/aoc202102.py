"""AoC 2, 2021"""

# Standard library imports
import pathlib
import sys

from dataclasses import dataclass
from aocd.models import Puzzle
from aocd import data, submit


@dataclass
class Submarine:
    """Class for keeping track of submarine position."""

    horizontal: int = 0
    depth: int = 0

    def forward(self, amount: int) -> None:
        self.horizontal += amount

    def up(self, amount: int) -> None:
        self.depth -= amount

    def down(self, amount: int) -> None:
        self.depth += amount

    def run_command(self, input: str):
        command_name, value = input.split(" ")
        do = f"{command_name}"
        if hasattr(self, do) and callable(func := getattr(self, do)):
            func(int(value))

    @property
    def current_position(self) -> int:
        return self.depth * self.horizontal


@dataclass
class Sub2(Submarine):
    """Part 2 submarine instructions.

    Based on your calculations, the planned course doesn't seem to make any sense. You find the submarine manual and
    discover that the process is actually slightly more complicated.

    In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0.
    The commands also mean something entirely different than you first thought:
    """

    aim: int = 0

    def forward(self, amount: int) -> None:
        """
        * forward X does two things:
          * It increases your horizontal position by X units.
          * It increases your depth by your aim multiplied by X.
        """
        self.horizontal += amount
        self.depth += (self.aim * amount)

    def up(self, amount: int) -> None:
        """up X decreases your aim by X units."""
        self.aim -= amount

    def down(self, amount: int) -> None:
        """down X increases your aim by X units."""
        self.aim += amount


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.splitlines()


def part1(data):
    """Solve part 1"""
    sub = Submarine()
    for command in data:
        sub.run_command(command)
    return sub.current_position


def part2(data):
    """Solve part 2"""
    sub = Sub2()
    for command in data:
        sub.run_command(command)
    return sub.current_position


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    answer_a, answer_b = solve(puzzle_input=data)
    print(answer_b)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
