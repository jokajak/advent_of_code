#!/usr/bin/env python

__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse
import copy
from functools import lru_cache

import pytest
import tqdm


def mask_write(mask, value):
    """Return masked valued

    Args:
        mask (bitstring): The bitmask for the value
        value (int): The value to be masked
    """
    bit_value = list(bin(value))
    # Strip off '0b'
    bit_value = bit_value[2:]
    # Pad the bit_value to match the length of the mask
    zero_pad = [0] * (len(mask) - len(bit_value))
    bit_value = zero_pad + bit_value
    for bit in range(-1, -len(mask) - 1, -1):
        if mask[bit] == "X":
            bit_value[bit] = str(bit_value[bit])
        if mask[bit] == "0":
            bit_value[bit] = "0"
        if mask[bit] == "1":
            bit_value[bit] = "1"
    return int("".join(bit_value), 2)


@lru_cache
def get_floating_addresses(bit_mask):
    calculated_values = set()
    if "X" not in set(bit_mask):
        return {bit_mask}
    # Convert to a list to ease operations
    bit_mask = list(bit_mask)
    for bit, val in enumerate(bit_mask):
        if val == "X":
            new_bitmask = copy.copy(bit_mask)
            new_bitmask[bit] = "0"
            calculated_values.update(get_floating_addresses("".join(new_bitmask)))
            new_bitmask[bit] = "1"
            calculated_values.update(get_floating_addresses("".join(new_bitmask)))
    return calculated_values


@lru_cache
def get_mask_writes(mask, location):
    """Implement memory mask decoder

    Args:
        mask (string): Mask
        location (int): Memory location to write
    Returns:
        ret (list): List of memory locations
    """
    locations = []
    # Convert location to bit list
    bit_value = list(bin(location))
    # Strip of '0b'
    bit_value = bit_value[2:]
    # Pad the bit_value to match the length of the mask
    zero_pad = [0] * (len(mask) - len(bit_value))
    bit_value = zero_pad + bit_value
    for bit in range(-1, -len(mask) - 1, -1):
        if mask[bit] == "X":
            bit_value[bit] = "X"
        elif mask[bit] == "0":
            bit_value[bit] = str(bit_value[bit])
        elif mask[bit] == "1":
            bit_value[bit] = "1"
    floating_writes = get_floating_addresses("".join(bit_value))
    for location in floating_writes:
        locations.append(int("".join(location), 2))
    return locations


def part_one(commands):
    mem = {}
    mask = "X" * 36
    for entry in tqdm.tqdm(commands):
        command, value = entry.split("=")
        if command.startswith("mask"):
            mask = value
            continue
        value = int(value.strip())
        new_value = mask_write(mask, value)
        location = command[4:-2]
        mem[location] = new_value
    total_value = 0
    for k in mem:
        total_value += mem[k]
    return total_value


def part_two(commands):
    mem = {}
    mask = "0" * 36
    for entry in tqdm.tqdm(commands):
        command, value = entry.split("=")
        value = value.strip()
        if command.startswith("mask"):
            mask = value
            continue
        location = int(command[4:-2])
        mem_locations = get_mask_writes(mask, location)
        for location in mem_locations:
            mem[location] = int(value)
    total_value = 0
    for k in mem:
        total_value += mem[k]
    return total_value


def main(args):
    """Main program flow

    Args:
        args (argparse.Namespace): Parsed arguments
    """
    lines = []
    for line in args.file.readlines():
        line = line.strip("\n")
        lines.append(line)

    print(part_one(lines))
    print(part_two(lines))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument(
        "--file",
        type=argparse.FileType("r"),
        help="Input file",
        default="2020/inputs/5",
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)


# TESTS


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            [
                "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
                "mem[8] = 11",
                "mem[7] = 101",
                "mem[8] = 0",
            ],
            165,
        )
    ],
)
def test_part_one(input, expected):
    assert part_one(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 11), 73),
        (("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 101), 101),
        (("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 0), 64),
    ],
)
def test_mask(input, expected):
    mask, value = input
    assert mask_write(mask, value) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            ("000000000000000000000000000000X1001X", 42),
            [26, 27, 58, 59],
        ),
    ],
)
def test_get_mask_writes(input, expected):
    mask, value = input
    assert get_mask_writes(mask, value) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            "000000000000000000000000000000X1101X",
            [
                "000000000000000000000000000000011010",
                "000000000000000000000000000000011011",
                "000000000000000000000000000000111010",
                "000000000000000000000000000000111011",
            ],
        ),
    ],
)
def test_get_floating_addresses(input, expected):
    assert sorted(get_floating_addresses(input)) == sorted(expected)


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            [
                "mask = 000000000000000000000000000000X1001X",
                "mem[42] = 100",
                "mask = 00000000000000000000000000000000X0XX",
                "mem[26] = 1",
            ],
            208,
        ),
    ],
)
def test_part_two(input, expected):
    assert part_two(input) == expected
