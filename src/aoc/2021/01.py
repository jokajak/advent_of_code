#!/usr/bin/env python
"""AoC 1, 2021.
Created: 2022-11-19 23:46:24.024475

# --- Day 1: Sonar Sweep ---
You're minding your own business on a ship at sea when the overboard
alarm goes off! You rush to see if you can help. Apparently, one of
the Elves tripped and accidentally sent the sleigh keys flying into
the ocean!
Before you know it, you're inside a submarine the Elves keep ready for
 situations like this. It's covered in Christmas lights (because of
course it is), and it even has an experimental antenna that should be
able to track the keys if you can boost its signal strength high
enough; there's a little meter that indicates the antenna's signal
strength by displaying 0-50 *stars*.
Your instincts tell you that in order to save Christmas, you'll need
to get all *fifty stars* by December 25th.
Collect stars by solving puzzles.  Two puzzles will be made available
on each day in the Advent calendar; the second puzzle is unlocked when
 you complete the first.  Each puzzle grants *one star*. Good luck!
As the submarine drops below the surface of the ocean, it
automatically performs a sonar sweep of the nearby sea floor. On a
small screen, the sonar sweep report (your puzzle input) appears: each
 line is a measurement of the sea floor depth as the sweep looks
further and further away from the submarine.
For example, suppose you had the following report:
```
199
200
208
210
200
207
240
269
260
263
```
This report indicates that, scanning outward from the submarine, the
sonar sweep found depths of `199`, `200`, `208`, `210`, and so on.
The first order of business is to figure out how quickly the depth
increases, just so you know what you're dealing with - you never know
if the keys will get *carried into deeper water* by an ocean current
or a fish or something.
To do this, count *the number of times a depth measurement increases*
from the previous measurement. (There is no measurement before the
first measurement.) In the example above, the changes are as follows:
```
199 (N/A - no previous measurement)
200 (increased)
208 (increased)
210 (increased)
200 (decreased)
207 (increased)
240 (increased)
269 (increased)
260 (decreased)
263 (increased)
```
In this example, there are *`7`* measurements that are larger than the
 previous measurement.
*How many measurements are larger than the previous measurement?*
"""

# Standard library imports
from aocd.models import Puzzle
from aocd import numbers


def parse(input_data):
    """Transform the data"""
    return numbers


def solve_part_one(input_data):
    """Solve part one."""
    answer = None
    previous_line = 0
    # Start at -1 so that the first line doesn't count
    number_increased = -1
    for line in input_data:
        # print("%d + %d = %d" % (num_one, num_two, num_one + num_two))
        if line > previous_line:
            number_increased += 1
        previous_line = line
    answer = number_increased
    return answer


def solve_part_two(input_data):
    """Solve part two."""
    answer = None
    index = 3
    last_depth = 0
    # Start at -1 so that the first line doesn't count
    number_increased = 0
    while index < len(input_data):
        current_depth = sum(input_data[index - 3 : index])
        if current_depth > last_depth:
            number_increased += 1
        last_depth = current_depth
        index += 1
    answer = number_increased
    return answer


def main():
    puzzle = Puzzle(year=2021, day=1)
    parsed_data = parse(puzzle.input_data)
    answer_a = solve_part_one(parsed_data)
    if answer_a:
        puzzle.answer_a = answer_a
    answer_b = solve_part_two(parsed_data)
    if answer_b:
        puzzle.answer_b = answer_b


if __name__ == "__main__":
    main()
