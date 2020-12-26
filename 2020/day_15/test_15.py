#!/usr/bin/env python3

import pytest
from tqdm import tqdm


def part_one(numbers, turns=2020):
    numbers_seen = {}
    for turn, number in enumerate(numbers[:-1]):
        numbers_seen[number] = turn
    last_number_spoken = numbers[-1]
    for turn in tqdm(range(len(numbers), turns)):
        last_turn_seen = numbers_seen.get(last_number_spoken, None)
        numbers_seen[last_number_spoken] = turn - 1
        if last_turn_seen is None:
            last_number_spoken = 0
        else:
            last_number_spoken = (turn - 1) - last_turn_seen
    return last_number_spoken


@pytest.mark.parametrize(
    "input, turns, expected",
    [
        ([0, 3, 6], 10, 0),
        ([1, 3, 2], 2020, 1),
        ([2, 1, 3], 2020, 10),
        ([1, 2, 3], 2020, 27),
        ([2, 3, 1], 2020, 78),
        ([3, 2, 1], 2020, 438),
        ([3, 1, 2], 2020, 1836),
    ],
)
def test_part_one(input, turns, expected):
    assert part_one(input, turns) == expected


#numbers = [1,2,16,19,18,0]
#print(part_one(numbers))
#print(part_one(numbers, turns=30000000))
