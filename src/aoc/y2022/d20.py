#!/usr/bin/env python
"""Solutions for AoC 20, 2022."""
# Created: 2022-12-20 09:42:55.797270

from typing import Tuple

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import inspect
from rich import print as rprint
from rich.progress import track

from aoc.utils import CircularLinkedList
from aoc.utils import MyNode as Node


class Msg(CircularLinkedList):
    def __init__(self, instructions: list):
        self.head: Node = None
        # Mapping of instruction to node
        self.indexes: dict[int, Node] = {}

        prev = None
        for idx, instruction in enumerate(instructions):
            node = Node(instruction)
            node.previous = prev
            self.indexes[(idx, instruction)] = node
            if prev:
                prev.next = node
            else:
                self.head = node
            prev = node
        if prev.next is None:
            prev.next = self.head
            self.head.previous = prev

    def __getitem__(self, key):
        return self.indexes[key]

    def __len__(self):
        return len(self.indexes)


def rearrange(linked_list: Msg, instruction: int, idx: int, modifier: int = 1):
    """Given instruction, rearrange a linked list"""
    node = linked_list.indexes[(idx, instruction)]
    offset = (instruction * modifier) % (len(linked_list) - 1)
    insertion_node = node + offset
    if node == insertion_node:
        return linked_list
    # Remove the current node from the list
    next_node = node.next
    previous_node = node.previous
    previous_node.next = node.next
    next_node.previous = node.previous

    # Move through the linked list
    # Put the current node between the insertion node and its next
    node.next = insertion_node.next
    node.previous = insertion_node
    # Update the A -> N -> C node
    insertion_node.next.previous = node
    # Update the A node
    insertion_node.next = node
    return linked_list


def parse(input_data):
    """Transform the data"""
    input_data = input_data.splitlines()
    instructions = list(map(int, input_data))
    linked_list = Msg(instructions)
    return instructions, linked_list


def solve_part_one(input_data):
    """Solve part one.

        # --- Day 20: Grove Positioning System ---
    It's finally time to meet back up with the Elves. When you try to
    contact them, however, you get no reply. Perhaps you're out of range?
    You know they're headed to the grove where the *star* fruit grows, so
    if you can figure out where that is, you should be able to meet back
    up with them.
    Fortunately, your handheld device has a file (your puzzle input) that
    contains the grove's coordinates! Unfortunately, the file is
    *encrypted* - just in case the device were to fall into the wrong
    hands.
    Maybe you can *decrypt* it?
    When you were still back at the camp, you overheard some Elves talking
     about coordinate file encryption. The main operation involved in
    decrypting the file is called *mixing*.
    The encrypted file is a list of numbers. To *mix* the file, move each
    number forward or backward in the file a number of positions equal to
    the value of the number being moved. The list is *circular*, so moving
     a number off one end of the list wraps back around to the other end
    as if the ends were connected.
    For example, to move the `1` in a sequence like `4, 5, 6, 1, 7, 8, 9`,
     the `1` moves one position forward: `4, 5, 6, 7, 1, 8, 9`. To move
    the `-2` in a sequence like `4, -2, 5, 6, 7, 8, 9`, the `-2` moves two
     positions backward, wrapping around: `4, 5, 6, 7, 8, -2, 9`.
    The numbers should be moved *in the order they originally appear* in
    the encrypted file. Numbers moving around during the mixing process do
     not change the order in which the numbers are moved.
    Consider this encrypted file:
    ```
    1
    2
    -3
    3
    -2
    0
    4
    ```
    Mixing this file proceeds as follows:
    ```
    Initial arrangement:
    1, 2, -3, 3, -2, 0, 4
    1 moves between 2 and -3:
    2, 1, -3, 3, -2, 0, 4
    2 moves between -3 and 3:
    1, -3, 2, 3, -2, 0, 4
    -3 moves between -2 and 0:
    1, 2, 3, -2, -3, 0, 4
    3 moves between 0 and 4:
    1, 2, -2, -3, 0, 3, 4
    -2 moves between 4 and 1:
    1, 2, -3, 0, 3, 4, -2
    0 does not move:
    1, 2, -3, 0, 3, 4, -2
    4 moves between -3 and 0:
    1, 2, -3, 4, 0, 3, -2
    ```
    Then, the grove coordinates can be found by looking at the 1000th,
    2000th, and 3000th numbers after the value `0`, wrapping around the
    list as necessary. In the above example, the 1000th number after `0`
    is `4`, the 2000th is `-3`, and the 3000th is `2`; adding these
    together produces `3`.
    Mix your encrypted file exactly once. *What is the sum of the three
    numbers that form the grove coordinates?*
    """
    instructions, linked_list = input_data

    start = None
    for idx, instruction in track(
        enumerate(instructions), description="Processing instructions"
    ):
        if instruction == 0:
            start = (idx, instruction)
        linked_list = rearrange(linked_list, instruction, idx)

    node = linked_list[start]
    total = 0
    print(len(linked_list))
    for v in [1000, 2000, 3000]:
        addend = v % len(linked_list)
        num = node + addend
        total += (num).data
        print(num)

    answer = total
    return answer


def solve_part_two(input_data):
    """Solve part two.

    The grove coordinate values seem nonsensical. While you ponder the mysteries of Elf encryption, you suddenly remember the rest of the decryption routine you overheard back at camp.

    First, you need to apply the decryption key, 811589153. Multiply each number by the decryption key before you begin; this will produce the actual list of numbers to mix.

    Second, you need to mix the list of numbers ten times. The order in which the numbers are mixed does not change during mixing; the numbers are still moved in the order they appeared in the original, pre-mixed list. (So, if -3 appears fourth in the original list of numbers to mix, -3 will be the fourth number to move during each round of mixing.)

    Using the same example as above:

    Initial arrangement:
    811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612

    After 1 round of mixing:
    0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153

    After 2 rounds of mixing:
    0, 2434767459, 1623178306, 3246356612, -2434767459, -1623178306, 811589153

    After 3 rounds of mixing:
    0, 811589153, 2434767459, 3246356612, 1623178306, -1623178306, -2434767459

    After 4 rounds of mixing:
    0, 1623178306, -2434767459, 811589153, 2434767459, 3246356612, -1623178306

    After 5 rounds of mixing:
    0, 811589153, -1623178306, 1623178306, -2434767459, 3246356612, 2434767459

    After 6 rounds of mixing:
    0, 811589153, -1623178306, 3246356612, -2434767459, 1623178306, 2434767459

    After 7 rounds of mixing:
    0, -2434767459, 2434767459, 1623178306, -1623178306, 811589153, 3246356612

    After 8 rounds of mixing:
    0, 1623178306, 3246356612, 811589153, -2434767459, 2434767459, -1623178306

    After 9 rounds of mixing:
    0, 811589153, 1623178306, -2434767459, 3246356612, 2434767459, -1623178306

    After 10 rounds of mixing:
    0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153

    The grove coordinates can still be found in the same way. Here, the 1000th number after 0 is 811589153, the 2000th is 2434767459, and the 3000th is -1623178306; adding these together produces 1623178306.

    Apply the decryption key and mix your encrypted file ten times. What is the sum of the three numbers that form the grove coordinates?
    """
    instructions, linked_list = input_data
    decryption_key = 811589153

    start = None
    for i in range(10):
        for idx, instruction in track(
            enumerate(instructions), description="Processing instructions"
        ):
            if not start and instruction == 0:
                start = (idx, instruction)
            linked_list = rearrange(
                linked_list, instruction, idx, modifier=decryption_key
            )

    node = linked_list[start]
    total = 0
    print(len(linked_list))
    for v in [1000, 2000, 3000]:
        addend = v % len(linked_list)
        num = node + addend
        total += (num).data * decryption_key

    answer = total
    return answer


def main():
    puzzle = Puzzle(year=2022, day=20)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2022).get((2022, 20), {})
    if stats.get("a", None) is None:
        answer_a = solve_part_one(parsed_data)
        if answer_a:
            puzzle.answer_a = answer_a
    if stats.get("b", None) is None:
        parsed_data = parse(puzzle.input_data)
        answer_b = solve_part_two(parsed_data)
        if answer_b:
            puzzle.answer_b = answer_b


if __name__ == "__main__":
    main()
