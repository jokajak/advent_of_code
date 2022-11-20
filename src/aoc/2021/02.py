#!/usr/bin/env python
"""AoC 2, 2021.
Created: 2022-11-20 10:28:47.286209

# --- Day 2: Dive! ---
Now, you need to figure out how to *pilot this thing*.
It seems like the submarine can take a series of commands like
`forward 1`, `down 2`, or `up 3`:
 - `forward X` increases the horizontal position by `X` units.
 - `down X` *increases* the depth by `X` units.
 - `up X` *decreases* the depth by `X` units.
Note that since you're on a submarine, `down` and `up` affect your
*depth*, and so they have the opposite result of what you might
expect.
The submarine seems to already have a planned course (your puzzle
input). You should probably figure out where it's going. For example:
```
forward 5
down 5
forward 8
up 3
down 8
forward 2
```
Your horizontal position and depth both start at `0`. The steps above
would then modify them as follows:
 - `forward 5` adds `5` to your horizontal position, a total of `5`.
 - `down 5` adds `5` to your depth, resulting in a value of `5`.
 - `forward 8` adds `8` to your horizontal position, a total of `13`.
 - `up 3` decreases your depth by `3`, resulting in a value of `2`.
 - `down 8` adds `8` to your depth, resulting in a value of `10`.
 - `forward 2` adds `2` to your horizontal position, a total of `15`.
After following these instructions, you would have a horizontal
position of `15` and a depth of `10`. (Multiplying these together
produces `150`.)
Calculate the horizontal position and depth you would have after
following the planned course. *What do you get if you multiply your
final horizontal position by your final depth?*
"""

# Standard library imports
from aocd.models import Puzzle
from aocd import lines

from dataclasses import dataclass


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


def parse(input_data):
    """Transform the data"""
    return lines


def solve_part_one(input_data):
    """Solve part one."""
    answer = None
    sub = Submarine()
    for command in input_data:
        sub.run_command(command)
    answer = sub.current_position
    return answer


def solve_part_two(input_data):
    """Solve part two."""
    answer = None
    return answer


def main():
    puzzle = Puzzle(year=2021, day=2)
    parsed_data = parse(puzzle.input_data)
    answer_a = solve_part_one(parsed_data)
    if answer_a:
        puzzle.answer_a = answer_a
    answer_b = solve_part_two(parsed_data)
    if answer_b:
        puzzle.answer_b = answer_b


if __name__ == "__main__":
    main()
