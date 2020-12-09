#!/usr/bin/env python

# --- Day 8: Handheld Halting ---
# Your flight to the major airline hub reaches cruising altitude without incident. While you consider checking the
# in-flight menu for one of those drinks that come with a little umbrella, you are interrupted by the kid sitting next
# to you.
#
# Their handheld game console won't turn on! They ask if you can take a look.
#
# You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of the device. You should
# be able to fix it, but first you need to be able to run the code in isolation.
#
# The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an
# operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).
#
# acc increases or decreases a single global value called the accumulator by the value given in the argument. For
# example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction, the
# instruction immediately below it is executed next.
#
# jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument as an
# offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue to the
# instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
#
# nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
# For example, consider the following program:
#
# nop +0
# acc +1
# jmp +4
# acc +3
# jmp -3
# acc -99
# acc +1
# jmp -4
# acc +6
#
# These instructions are visited in this order:
#
# nop +0  | 1
# acc +1  | 2, 8(!)
# jmp +4  | 3
# acc +3  | 6
# jmp -3  | 7
# acc -99 |
# acc +1  | 4
# jmp -4  | 5
# acc +6  |
#
# First, the nop +0 does nothing. Then, the accumulator is increased from 0 to 1 (acc +1) and jmp +4 sets the next
# instruction to the other acc +1 near the bottom. After it increases the accumulator from 1 to 2, jmp -4 executes,
# setting the next instruction to the only acc +3. It sets the accumulator to 5, and jmp -3 causes the program to
# continue back at the first acc +1.
#
# This is an infinite loop: with this sequence of jumps, the program will run forever. The moment the program tries to
# run any instruction a second time, you know it will never terminate.
#
# Immediately before the program would run an instruction a second time, the value in the accumulator is 5.
#
# Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the
# accumulator?

__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse

import pytest


def boot_code(instructions):
    """Calculate accumulator value from boot code

    Args:
        instructions (list): List of instructions
    """
    visited_positions = set()
    accumulator_value = 0
    current_index = 0
    while current_index not in visited_positions and current_index < len(instructions):
        current_instruction = instructions[current_index].split(" ")
        visited_positions.add(current_index)

        if current_instruction[0] == "nop":
            current_index += 1
            continue
        operation, value = current_instruction
        value = int(value)
        if operation.startswith("acc"):
            accumulator_value += value
            current_index += 1
            continue
        if operation.startswith("jmp"):
            current_index += value
            continue
    return accumulator_value, current_index


def mangle_boot(instructions):
    target_termination_index = len(instructions)
    for instruction_pointer, instruction in enumerate(instructions):
        current_instruction = instruction.split(" ")
        accumulator, final_index = boot_code(instructions)
        if final_index == target_termination_index:
            return accumulator
        if current_instruction[0] == "nop":
            new_instruction = "jmp {}".format(current_instruction[1])
            instructions[instruction_pointer] = new_instruction
            accumulator, final_index = boot_code(instructions)
            if final_index == target_termination_index:
                return accumulator
            else:
                new_instruction = "nop {}".format(current_instruction[1])
                instructions[instruction_pointer] = new_instruction
        elif current_instruction[0] == "jmp":
            new_instruction = "nop {}".format(current_instruction[1])
            instructions[instruction_pointer] = new_instruction
            accumulator, final_index = boot_code(instructions)
            if final_index == target_termination_index:
                return accumulator
            else:
                new_instruction = "jmp {}".format(current_instruction[1])
                instructions[instruction_pointer] = new_instruction
    return False


def main(args):
    """Main program flow

    Args:
        args (argparse.Namespace): Parsed arguments
    """
    instructions = []
    for line in args.file.readlines():
        line = line.strip("\n")
        instructions.append(line)
    print(boot_code(instructions))

    # --- Part Two ---
    # After some careful analysis, you believe that exactly one instruction is corrupted.
    #
    # Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp. (No acc instructions were harmed in the corruption of this boot code.)
    #
    # The program is supposed to terminate by attempting to execute an instruction immediately after the last instruction in the file. By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.
    #
    # For example, consider the same program from above:
    #
    # nop +0
    # acc +1
    # jmp +4
    # acc +3
    # jmp -3
    # acc -99
    # acc +1
    # jmp -4
    # acc +6
    # If you change the first instruction from nop +0 to jmp +0, it would create a single-instruction infinite loop, never leaving that instruction. If you change almost any of the jmp instructions, the program will still eventually find another jmp instruction and loop forever.
    #
    # However, if you change the second-to-last instruction (from jmp -4 to nop -4), the program terminates! The instructions are visited in this order:
    #
    # nop +0  | 1
    # acc +1  | 2
    # jmp +4  | 3
    # acc +3  |
    # jmp -3  |
    # acc -99 |
    # acc +1  | 4
    # nop -4  | 5
    # acc +6  | 6
    # After the last instruction (acc +6), the program terminates by attempting to run the instruction below the last instruction in the file. With this change, after the program terminates, the accumulator contains the value 8 (acc +1, acc +1, acc +6).
    #
    # Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?
    #
    #
    print(mangle_boot(instructions))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("--file", type=argparse.FileType("r"), help="Input file", default="2020/inputs/8")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)


# TESTS

@pytest.mark.parametrize("input, expected", [
    ([
        "nop +0",
        "acc +1",
        "jmp +4",
        "acc +3",
        "jmp -3",
        "acc -99",
        "acc +1",
        "jmp -4",
        "acc +6",
    ], (5, 1)
    ),
    (["nop +0"], (0, 1)),
])
def test_boot_code(input, expected):
    assert boot_code(input) == expected

@pytest.mark.parametrize("input, expected", [
    ([
        "nop +0",
        "acc +1",
        "jmp +4",
        "acc +3",
        "jmp -3",
        "acc -99",
        "acc +1",
        "jmp -4",
        "acc +6",
    ], 8
    ),
    (["nop +0"], 0),
])
def test_mangle_boot(input, expected):
    assert mangle_boot(input) == expected
