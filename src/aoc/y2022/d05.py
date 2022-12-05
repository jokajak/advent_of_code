#!/usr/bin/env python
"""Solutions for AoC 5, 2022."""
# Created: 2022-12-05 08:46:43.600251

from collections import deque

# Standard library imports
from aocd.models import Puzzle


def parse_initialization(input_data):
    """Transform the data.

    Convert:
        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3
    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2

    To
    expected = [
        ["Z", "N"],
        ["M", "C", "D"],
        ["P"],
    ]
    """
    parsed = {}
    # Read each line
    for line in input_data.splitlines():
        # Each position is 4 characters wide, so count by 4
        for i in range(0, len(line), 4):
            if line[i] == "[":
                if i in parsed:
                    parsed[i].insert(0, line[i + 1])
                else:
                    parsed[i] = [line[i + 1]]
    ret = []
    for i in range(0, len(parsed)):
        ret.append(parsed[i * 4])
    return ret


def parse_steps(input_data):
    """Transform the data.

    Convert:
        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3
    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2

    To
    [
        (1, 2, 1),
        (3, 1, 3),
        (2, 2, 1),
        (1, 1, 2),
    ]
    """
    parsed = []
    for line in input_data.splitlines():
        if line.startswith("move"):
            line = line.split(" ")
            count, source, dest = line[1], line[3], line[5]
            parsed.append((int(count), int(source), int(dest)))
    return parsed


def parse(input_data):
    """Transform the data.

    Convert:
        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3
    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2

    To
    expected = [
        ["Z", "N"],
        ["M", "C", "D"],
        ["P"],
    ],
    [
        (1, 2, 1),
        (3, 1, 3),
        (2, 2, 1),
        (1, 1, 2),
    ]
    """
    initialization_state = parse_initialization(input_data)
    steps = parse_steps(input_data)
    return initialization_state, steps


def process_instruction(current_state, instruction):
    """Given a current state and instruction, perform the algorithm."""
    count, source, dest = instruction
    # Fix offsets
    source, dest = source - 1, dest - 1
    if count == 0:
        return current_state
    for i in range(0, count, 1):
        item = current_state[source].pop()
        current_state[dest].append(item)
    return current_state


def solve_part_one(input_data):
    """Solve part one.

        # --- Day 5: Supply Stacks ---
    The expedition can depart as soon as the final supplies have been
    unloaded from the ships. Supplies are stored in stacks of marked
    *crates*, but because the needed supplies are buried under many other
    crates, the crates need to be rearranged.
    The ship has a *giant cargo crane* capable of moving crates between
    stacks. To ensure none of the crates get crushed or fall over, the
    crane operator will rearrange them in a series of carefully-planned
    steps. After the crates are rearranged, the desired crates will be at
    the top of each stack.
    The Elves don't want to interrupt the crane operator during this
    delicate procedure, but they forgot to ask her *which* crate will end
    up where, and they want to be ready to unload them as soon as possible
     so they can embark.
    They do, however, have a drawing of the starting stacks of crates
    *and* the rearrangement procedure (your puzzle input). For example:
    ```
        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3
    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2
    ```
    In this example, there are three stacks of crates. Stack 1 contains
    two crates: crate `Z` is on the bottom, and crate `N` is on top. Stack
     2 contains three crates; from bottom to top, they are crates `M`,
    `C`, and `D`. Finally, stack 3 contains a single crate, `P`.
    Then, the rearrangement procedure is given. In each step of the
    procedure, a quantity of crates is moved from one stack to a different
     stack. In the first step of the above rearrangement procedure, one
    crate is moved from stack 2 to stack 1, resulting in this
    configuration:
    ```
    [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3
    ```
    In the second step, three crates are moved from stack 1 to stack 3.
    Crates are moved *one at a time*, so the first crate to be moved (`D`)
     ends up below the second and third crates:
    ```
            [Z]
            [N]
        [C] [D]
        [M] [P]
     1   2   3
    ```
    Then, both crates are moved from stack 2 to stack 1. Again, because
    crates are moved *one at a time*, crate `C` ends up below crate `M`:
    ```
            [Z]
            [N]
    [M]     [D]
    [C]     [P]
     1   2   3
    ```
    Finally, one crate is moved from stack 1 to stack 2:
    ```
            [Z]
            [N]
            [D]
    [C] [M] [P]
     1   2   3
    ```
    The Elves just need to know *which crate will end up on top of each
    stack*; in this example, the top crates are `C` in stack 1, `M` in
    stack 2, and `Z` in stack 3, so you should combine these together and
    give the Elves the message `CMZ`.
    *After the rearrangement procedure completes, what crate ends up on
    top of each stack?*
    """
    state, instructions = input_data
    for instruction in instructions:
        state = process_instruction(state, instruction)

    answer = ""
    for i in range(0, len(state), 1):
        answer = answer + state[i].pop()
    return answer


def solve_part_two(input_data):
    """Solve part two.

    As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

    Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

    The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

    Again considering the example above, the crates begin in the same configuration:

        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3

    Moving a single crate from stack 2 to stack 1 behaves the same as before:

    [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3

    However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order, resulting in this new configuration:

            [D]
            [N]
        [C] [Z]
        [M] [P]
     1   2   3

    Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

            [D]
            [N]
    [C]     [Z]
    [M]     [P]
     1   2   3

    Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

            [D]
            [N]
            [Z]
    [M] [C] [P]
     1   2   3

    In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

    Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?
    """

    def process_instruction(current_state, instruction):
        """Given a current state and instruction, perform the algorithm."""
        count, source, dest = instruction
        # Fix offsets
        source, dest = source - 1, dest - 1
        # Make sure our data is sane
        if len(current_state[source]) == 0:
            return current_state
        left, right = current_state[source][:-count], current_state[source][-count:]
        current_state[source] = left
        current_state[dest] += right
        return current_state

    print(input_data)
    state, instructions = input_data
    print("Initial state")
    for i, col in enumerate(state):
        print(f"{i+1}: {''.join(col)}")
    ret = input()
    # ret = "c"
    for instruction in instructions:
        print(f"Parsing {instruction}")
        state = process_instruction(state, instruction)
        for i, col in enumerate(state):
            print(f"{i+1}: {''.join(col)}")
        if ret != "c":
            ret = input()

    answer = ""
    for i in range(0, len(state), 1):
        if len(state[i]) > 0:
            answer = answer + state[i].pop()
    return answer


def main():
    puzzle = Puzzle(year=2022, day=5)
    parsed_data = parse(puzzle.input_data)
    answer_a = solve_part_one(parsed_data)
    if answer_a:
        puzzle.answer_a = answer_a
    parsed_data = parse(puzzle.input_data)
    answer_b = solve_part_two(parsed_data)
    if answer_b:
        puzzle.answer_b = answer_b


if __name__ == "__main__":
    main()
