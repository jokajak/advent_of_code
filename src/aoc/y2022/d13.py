#!/usr/bin/env python
"""Solutions for AoC 13, 2022."""
# Created: 2022-12-13 07:52:06.700698

import functools

# Standard library imports
from aocd.models import Puzzle

from aoc.utils.parsers import str_to_list


def parse(input_data: str):
    """Transform the data

    [1,1,3,1,1]
    [1,1,5,1,1]
    [[1],[2,3,4]]
    [[1],4]

    becomes:
    [
        ( [1,1,3,1,1], [1,1,5,1,1])
        ([[1],[2,3,4]], [[1],4])
    ]
    """
    ret = []
    lines = input_data.splitlines()
    for i in range(0, len(lines), 3):
        left = eval(lines[i])
        right = eval(lines[i + 1])
        ret.append((left, right))

    return ret


def is_ordered(left, right):
    """Compare order of two entries

    *Packet data consists of lists and integers.* Each list starts with
    `[`, ends with `]`, and contains zero or more comma-separated values
    (either integers or other lists). Each packet is always a list and
    appears on its own line.
    When comparing two values, the first value is called *left* and the
    second value is called *right*. Then:
     - If *both values are integers*, the *lower integer* should come
    first. If the left integer is lower than the right integer, the inputs
     are in the right order. If the left integer is higher than the right
    integer, the inputs are not in the right order. Otherwise, the inputs
    are the same integer; continue checking the next part of the input.
     - If *both values are lists*, compare the first value of each list,
    then the second value, and so on. If the left list runs out of items
    first, the inputs are in the right order. If the right list runs out
    of items first, the inputs are not in the right order. If the lists
    are the same length and no comparison makes a decision about the
    order, continue checking the next part of the input.
     - If *exactly one value is an integer*, convert the integer to a list
     which contains that integer as its only value, then retry the
    comparison. For example, if comparing `[0,0,0]` and `2`, convert the
    right value to `[2]` (a list containing `2`); the result is then found
     by instead comparing `[0,0,0]` and `[2]`.
    - Compare [1,1,3,1,1] vs [1,1,5,1,1]
      - Compare 1 vs 1
      - Compare 1 vs 1
      - Compare 3 vs 5
        - Left side is smaller, so inputs are in the right order
    """
    print(f"Comparing {left} {right}")
    if len(left) > 0 and len(right) == 0:
        return False
    elif len(left) == 0 and len(right) > 0:
        return True
    elif len(left) == 0 and len(right) == 0:
        return None
    for i in range(len(left)):
        if i >= len(right):
            return False
        try:
            left_val, right_val = left[i], right[i]
        except IndexError:
            print(f"Too far: {i} {left} {right} {i >= len(right)}")
            raise
        left_type, right_type = type(left_val), type(right_val)
        if left_type == right_type == int:
            if left_val < right_val:
                return True
            elif left_val == right_val:
                continue
            elif left_val > right_val:
                return False
        elif left_type == right_type == list:
            ret = is_ordered(left_val, right_val)
            print(f"Compared {left_val} {right_val} => {ret}")
            if ret is not None:
                return ret
            else:
                continue
        elif left_type == list and right_type == int:
            print("Type mismatch")
            new_right = [v if j != i else [right_val] for j, v in enumerate(right)]
            ret = is_ordered(left, new_right)
            if ret is not None:
                return ret
            else:
                continue
        elif left_type == int and right_type == list:
            print("Type mismatch")
            new_left = [v if j != i else [left_val] for j, v in enumerate(left)]
            ret = is_ordered(new_left, right)
            if ret is not None:
                return ret
            else:
                continue
    else:
        # Equal values, need to check length now
        if len(right) > len(left):
            return True
        else:
            return None

    raise ValueError("Should not reach", left, right)


def solve_part_one(input_data):
    """Solve part one.

        # --- Day 13: Distress Signal ---
    You climb the hill and again try contacting the Elves. However, you
    instead receive a signal you weren't expecting: a *distress signal*.
    Your handheld device must still not be working properly; the packets
    from the distress signal got decoded *out of order*. You'll need to
    re-order the list of received packets (your puzzle input) to decode
    the message.
    Your list consists of pairs of packets; pairs are separated by a blank
     line. You need to identify *how many pairs of packets are in the
    right order*.
    For example:
    ```
    [1,1,3,1,1]
    [1,1,5,1,1]
    [[1],[2,3,4]]
    [[1],4]
    [9]
    [[8,7,6]]
    [[4,4],4,4]
    [[4,4],4,4,4]
    [7,7,7,7]
    [7,7,7]
    []
    [3]
    [[[]]]
    [[]]
    [1,[2,[3,[4,[5,6,7]]]],8,9]
    [1,[2,[3,[4,[5,6,0]]]],8,9]
    ```
    *Packet data consists of lists and integers.* Each list starts with
    `[`, ends with `]`, and contains zero or more comma-separated values
    (either integers or other lists). Each packet is always a list and
    appears on its own line.
    When comparing two values, the first value is called *left* and the
    second value is called *right*. Then:
     - If *both values are integers*, the *lower integer* should come
    first. If the left integer is lower than the right integer, the inputs
     are in the right order. If the left integer is higher than the right
    integer, the inputs are not in the right order. Otherwise, the inputs
    are the same integer; continue checking the next part of the input.
     - If *both values are lists*, compare the first value of each list,
    then the second value, and so on. If the left list runs out of items
    first, the inputs are in the right order. If the right list runs out
    of items first, the inputs are not in the right order. If the lists
    are the same length and no comparison makes a decision about the
    order, continue checking the next part of the input.
     - If *exactly one value is an integer*, convert the integer to a list
     which contains that integer as its only value, then retry the
    comparison. For example, if comparing `[0,0,0]` and `2`, convert the
    right value to `[2]` (a list containing `2`); the result is then found
     by instead comparing `[0,0,0]` and `[2]`.
    Using these rules, you can determine which of the pairs in the example
     are in the right order:
    ```
    == Pair 1 ==
    - Compare [1,1,3,1,1] vs [1,1,5,1,1]
      - Compare 1 vs 1
      - Compare 1 vs 1
      - Compare 3 vs 5
        - Left side is smaller, so inputs are in the right order
    == Pair 2 ==
    - Compare [[1],[2,3,4]] vs [[1],4]
      - Compare [1] vs [1]
        - Compare 1 vs 1
      - Compare [2,3,4] vs 4
        - Mixed types; convert right to [4] and retry comparison
        - Compare [2,3,4] vs [4]
          - Compare 2 vs 4
            - Left side is smaller, so inputs are in the right order
    == Pair 3 ==
    - Compare [9] vs [[8,7,6]]
      - Compare 9 vs [8,7,6]
        - Mixed types; convert left to [9] and retry comparison
        - Compare [9] vs [8,7,6]
          - Compare 9 vs 8
            - Right side is smaller, so inputs are not in the right order
    == Pair 4 ==
    - Compare [[4,4],4,4] vs [[4,4],4,4,4]
      - Compare [4,4] vs [4,4]
        - Compare 4 vs 4
        - Compare 4 vs 4
      - Compare 4 vs 4
      - Compare 4 vs 4
      - Left side ran out of items, so inputs are in the right order
    == Pair 5 ==
    - Compare [7,7,7,7] vs [7,7,7]
      - Compare 7 vs 7
      - Compare 7 vs 7
      - Compare 7 vs 7
      - Right side ran out of items, so inputs are not in the right order
    == Pair 6 ==
    - Compare [] vs [3]
      - Left side ran out of items, so inputs are in the right order
    == Pair 7 ==
    - Compare [[[]]] vs [[]]
      - Compare [[]] vs []
        - Right side ran out of items, so inputs are not in the right
    order
    == Pair 8 ==
    - Compare [1,[2,[3,[4,[5,6,7]]]],8,9] vs [1,[2,[3,[4,[5,6,0]]]],8,9]
      - Compare 1 vs 1
      - Compare [2,[3,[4,[5,6,7]]]] vs [2,[3,[4,[5,6,0]]]]
        - Compare 2 vs 2
        - Compare [3,[4,[5,6,7]]] vs [3,[4,[5,6,0]]]
          - Compare 3 vs 3
          - Compare [4,[5,6,7]] vs [4,[5,6,0]]
            - Compare 4 vs 4
            - Compare [5,6,7] vs [5,6,0]
              - Compare 5 vs 5
              - Compare 6 vs 6
              - Compare 7 vs 0
                - Right side is smaller, so inputs are not in the right
    order
    ```
    What are the indices of the pairs that are already *in the right
    order*? (The first pair has index 1, the second pair has index 2, and
    so on.) In the above example, the pairs in the right order are 1, 2,
    4, and 6; the sum of these indices is `13`.
    Determine which pairs of packets are already in the right order. *What
     is the sum of the indices of those pairs?*
    """
    answer = 0
    for i, entry in enumerate(input_data):
        pair = i + 1
        print(f"Testing pair {pair}")
        left, right = entry
        if is_ordered(left, right):
            print(f"{pair} {left} {right}: True")
            answer += pair
    return answer


def solve_part_two(input_data):
    """Solve part two.

    Now, you just need to put all of the packets in the right order. Disregard the blank lines in your list of received packets.

    The distress signal protocol also requires that you include two additional divider packets:

    [[2]]
    [[6]]

    Using the same rules as before, organize all packets - the ones in your list of received packets as well as the two divider packets - into the correct order.

    For the example above, the result of putting the packets in the correct order is:

    []
    [[]]
    [[[]]]
    [1,1,3,1,1]
    [1,1,5,1,1]
    [[1],[2,3,4]]
    [1,[2,[3,[4,[5,6,0]]]],8,9]
    [1,[2,[3,[4,[5,6,7]]]],8,9]
    [[1],4]
    [[2]]
    [3]
    [[4,4],4,4]
    [[4,4],4,4,4]
    [[6]]
    [7,7,7]
    [7,7,7,7]
    [[8,7,6]]
    [9]

    Afterward, locate the divider packets. To find the decoder key for this distress signal, you need to determine the indices of the two divider packets and multiply them together. (The first packet is at index 1, the second packet is at index 2, and so on.) In this example, the divider packets are 10th and 14th, and so the decoder key is 140.
    """

    class Packet:
        def __init__(self, packet):
            self.packet = packet

        def __lt__(self, o):
            return is_ordered(self.packet, o.packet)

        def __gt__(self, o):
            return is_ordered(o.packet, self.packet)

        def __eq__(self, o):
            return is_ordered(self.packet, o.packet) is None

    packets = []
    packets.append(Packet([[2]]))  # Start packet
    packets.append(Packet([[6]]))  # End packet
    for entry in input_data:
        left, right = entry
        packets.append(Packet(left))
        packets.append(Packet(right))
    packets = sorted(packets)
    ret = 1
    for i, packet in enumerate(packets):
        if packet == Packet([[2]]):
            ret = ret * (i + 1)
        elif packet == Packet([[6]]):
            ret = ret * (i + 1)
    answer = ret
    return answer


def main():
    puzzle = Puzzle(year=2022, day=13)
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
