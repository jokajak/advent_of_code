"""AoC 14, 2021"""

# Standard library imports
import pathlib
import sys
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Polymer:
    first_character: str
    last_character: str
    pairs: defaultdict
    rules: defaultdict


def parse(puzzle_input):
    """Parse input"""
    lines = puzzle_input.splitlines()
    polymer_template = lines[0]
    pair_insertion_rules = {}
    for rule in lines[1:]:
        if "->" not in rule:
            continue
        pair, element = rule.split(" -> ")
        pair = pair.strip()
        left_char, right_char = pair[0], pair[1]
        element = element.strip()
        pair_insertion_rules[pair] = (f"{left_char}{element}", f"{element}{right_char}")
    return polymer_template, pair_insertion_rules


# This works
def process_polymer_change(polymer: defaultdict, rules: dict) -> defaultdict:
    new_polymer = defaultdict(int)
    for pair in polymer.keys():
        # don't process empty pairs
        while polymer[pair] > 0:
            polymer[pair] -= 1
            new_pair_1, new_pair_2 = rules[pair]
            new_polymer[new_pair_1] += 1
            new_polymer[new_pair_2] += 1
    # assert (sum([v for v in polymer.values()])*2) == sum([v for v in new_polymer.values()])
    return new_polymer


def count_letters(polymer: defaultdict):
    letters = defaultdict(int)
    for pair, value in polymer.items():
        left_letter, right_letter = pair[0], pair[1]
        letters[left_letter] += value
        if left_letter != right_letter:
            letters[right_letter] += value
    return letters


def polymer_to_pairs(polymer: str) -> defaultdict:
    pairs = defaultdict(int)
    for i in range(len(polymer) - 1):
        pairs[polymer[i : i + 2]] += 1  # pull out two characters from the string
    return pairs


def iterate_polymer(polymer_pairs: defaultdict, rules: dict, steps: int = 1) -> defaultdict:
    """Process polymer pair steps"""
    # every pair insertion results in an increase in pair values and decrease in the initial pair value
    for step in range(steps):
        polymer_pairs = process_polymer_change(polymer_pairs, rules)
    return polymer_pairs


def part1(data, steps: int = 10) -> int:
    """Solve part 1

    The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B are
    immediately adjacent, element C should be inserted between them. These insertions all happen simultaneously.

    Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result.
    What do you get if you take the quantity of the most common element and subtract the quantity of the least common
    element?
    """
    polymer_template, rules = data
    pairs = polymer_to_pairs(polymer_template)

    pairs = iterate_polymer(pairs, rules, steps)
    letters = count_letters(pairs)
    max_letter_occurrence = -1
    max_letter = [k for k, v in letters.items() if v > max_letter_occurrence]
    min_letter_occurrence = letters[max_letter[0]]
    min_letter = [k for k, v in letters.items() if v < min_letter_occurrence]
    min_letter_occurrence = letters[min_letter[0]]
    return max_letter_occurrence - min_letter_occurrence


def part2(data):
    """Solve part 2"""


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
