#!/usr/bin/env python
"""Solutions for AoC 15, 2023."""
# Created: 2023-12-15 08:02:57.534817

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from collections import defaultdict, deque


def parse(input_data):
    """Transform the data"""
    return input_data.split(",")


def hash_string(input_string):
    """Calculate the hash of a string:

    Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256.
    """
    ret = 0
    for current_character in input_string:
        ret = ((ret + ord(current_character)) * 17) % 256
    return ret


def solve_part_one(input_data):
    """Solve part one.

    Calculate the sum of the hash of the initialization sequence. The hash is calculated by:

    Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256.

    """
    answer = 0
    for input_string in input_data:
        answer += hash_string(input_string)
    return answer


def solve_part_two(input_data):
    """Solve part two.

    The book goes on to explain how to perform each step in the initialization sequence, a process it calls the Holiday
    ASCII String Helper Manual Arrangement Procedure, or HASHMAP for short.

    Each step begins with a sequence of letters that indicate the label of the lens on which the step operates. The
    result of running the HASH algorithm on the label indicates the correct box for that step.

    The label will be immediately followed by a character that indicates the operation to perform: either an equals sign
    (=) or a dash (-).

    If the operation character is a dash (-), go to the relevant box and remove the lens with the given label if it is
    present in the box. Then, move any remaining lenses as far forward in the box as they can go without changing their
    order, filling any space made by removing the indicated lens. (If no lens in that box has the given label, nothing
    happens.)

    If the operation character is an equals sign (=), it will be followed by a number indicating the focal length of the
    lens that needs to go into the relevant box; be sure to use the label maker to mark the lens with the label given in
    the beginning of the step so you can find it later. There are two possible situations:

    If there is already a lens in the box with the same label, replace the old lens with the new lens: remove the old
    lens and put the new lens in its place, not moving any other lenses in the box.
    If there is not already a lens in the box with the same label, add the lens to the box immediately behind any lenses
    already in the box. Don't move any of the other lenses when you do this. If there aren't any lenses in the box, the
    new lens goes all the way to the front of the box.

    To confirm that all of the lenses are installed correctly, add up the focusing power of all of the lenses. The
    focusing power of a single lens is the result of multiplying together:

    One plus the box number of the lens in question.
    The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
    The focal length of the lens.
    """
    answer = 0
    # keep track of which labels are in each box
    light_boxes = []
    for _ in range(256):
        light_boxes.append(deque())
    # keep track of focal lengths
    focal_lengths = {}
    for input_string in input_data:
        if "=" in input_string:
            label, focal_length = input_string.split("=")
            label_hash = hash_string(label)
            focal_lengths[label] = int(focal_length)
            if label not in light_boxes[label_hash]:
                light_boxes[label_hash].append(label)
        if "-" in input_string:
            label, focal_length = input_string.split("-")
            label_hash = hash_string(label)
            if label in light_boxes[label_hash]:
                light_boxes[label_hash].remove(label)

    for box_number, light_box in enumerate(light_boxes):
        for slot_number, lens in enumerate(light_box):
            focusing_power = (1 + box_number) * (1 + slot_number) * focal_lengths[lens]
            answer += focusing_power

    return answer


def main():
    puzzle = Puzzle(year=2023, day=15)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 15), {})
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
