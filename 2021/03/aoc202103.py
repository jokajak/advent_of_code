"""AoC 3, 2021"""

# Standard library imports
import pathlib
import sys

from dataclasses import dataclass
from aocd import data, submit


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.splitlines()


def part1(data):
    """Solve part 1"""
    gamma_rate, epsilon_rate = [], []
    # assume all lines are the same length
    for index in range(len(data[0])):  # for each position in the first line
        gamma = 0
        for entry in data:
            if int(entry[index]) == 1:
                gamma += 1
            else:
                gamma -= 1
        if gamma > 0:
            gamma_rate.append("1")
            epsilon_rate.append("0")
        else:
            gamma_rate.append("0")
            epsilon_rate.append("1")
    return int("".join(gamma_rate), 2) * int("".join(epsilon_rate), 2)


def filter_entries(input: list, index: int):
    """Split list by frequency of most common bit"""
    one_entries, zero_entries = [], []
    for entry in input:
        if entry[index] == "0":
            zero_entries.append(entry)
        else:
            one_entries.append(entry)
    return zero_entries, one_entries


def part2(data):
    """Solve part 2.

    Next, you should verify the life support rating, which can be determined by multiplying the oxygen generator rating
    by the CO2 scrubber rating.

    Both the oxygen generator rating and the CO2 scrubber rating are values that can be found in your diagnostic report
    - finding them is the tricky part. Both values are located using a similar process that involves filtering out
    values until only one remains. Before searching for either rating value, start with the full list of binary numbers
    from your diagnostic report and consider just the first bit of those numbers. Then:

    Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard
    numbers which do not match the bit criteria. If you only have one number left, stop; this is the rating value for
    which you are searching. Otherwise, repeat the process, considering the next bit to the right. The bit criteria
    depends on which type of rating value you want to find:

    To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep only
    numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the position being
    considered. To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and
    keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in the
    position being considered. For example, to determine the oxygen generator rating value using the same example
    diagnostic report from above:

    Start with all 12 numbers and consider only the first bit of each number. There are more 1 bits (7) than 0 bits (5),
    so keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and 11001.
    Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3), so keep only
    the 4 numbers with a 0 in the second position: 10110, 10111, 10101, and 10000. In the third position, three of the
    four numbers have a 1, so keep those three: 10110, 10111, and 10101. In the fourth position, two of the three
    numbers have a 1, so keep those two: 10110 and 10111. In the fifth position, there are an equal number of 0 bits and
    1 bits (one each). So, to find the oxygen generator rating, keep the number with a 1 in that position: 10111. As
    there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal. Then, to determine the
    CO2 scrubber rating value from the same example above:

    Start again with all 12 numbers and consider only the first bit of each number. There are fewer 0 bits (5) than 1
    bits (7), so keep only the 5 numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and 01010. Then,
    consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0 bits (3), so keep only the 2
    numbers with a 1 in the second position: 01111 and 01010. In the third position, there are an equal number of 0 bits
    and 1 bits (one each). So, to find the CO2 scrubber rating, keep the number with a 0 in that position: 01010. As
    there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal. Finally, to find the life
    support rating, multiply the oxygen generator rating (23) by the CO2 scrubber rating (10) to get 230.

    Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating,
    then multiply them together. What is the life support rating of the submarine? (Be sure to represent your answer in
    decimal, not binary.)

    """
    generator_entries = data
    oxygen_generator_rating = None
    carbon_dioxide_generator_rating = None
    for _ in range(len(data)):
        for index in range(len(data[0])):
            zero_entries, one_entries = filter_entries(generator_entries, index)
            if len(one_entries) >= len(zero_entries):
                generator_entries = one_entries
            else:
                generator_entries = zero_entries
            if len(generator_entries) == 1:
                oxygen_generator_rating = int("".join(generator_entries[0]), 2)
                break
        if oxygen_generator_rating:
            break
    generator_entries = data
    for _ in range(len(data)):
        for index in range(len(data[0])):
            zero_entries, one_entries = filter_entries(generator_entries, index)
            if len(zero_entries) <= len(one_entries):
                generator_entries = zero_entries
            else:
                generator_entries = one_entries
            if len(generator_entries) == 1:
                carbon_dioxide_generator_rating = int("".join(generator_entries[0]), 2)
                break
        if carbon_dioxide_generator_rating:
            break

    return oxygen_generator_rating * carbon_dioxide_generator_rating


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
