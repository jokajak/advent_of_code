#!/usr/bin/env python

from collections import deque

import pytest
import tqdm


@pytest.mark.parametrize(
    "input, expected",
    [
        ([3, 8, 9, 1, 2, 5, 4, 6, 7], [2, 8, 9, 1, 5, 4, 6, 7, 3]),
        ([2, 8, 9, 1, 5, 4, 6, 7, 3], [5, 4, 6, 7, 8, 9, 1, 3, 2]),
    ],
)
def test_move(input, expected):
    input = deque(input)
    max_value = max(input)
    min_value = min(input)
    assert move(input, min_value, max_value) == deque(expected)


def move(input, min_value, max_value):
    current_value = input.popleft()
    insert_value = current_value
    insert_location = 1
    # make sure insert location isn't in the next 3 spots
    while insert_location < 3:
        insert_value = insert_value - 1
        if insert_value < min_value:
            insert_value = max_value
        insert_location = input.index(insert_value)
    # move insert location 3 spots left
    insert_location = insert_location - 2
    next_three = [input.popleft() for _ in range(3)]
    next_three.reverse()
    for entry in next_three:
        input.insert(insert_location, entry)
    input.appendleft(current_value)
    input.rotate(-1)
    return input


def perform_moves(input, moves):
    min_value, max_value = min(input), max(input)
    for _ in tqdm.tqdm(range(moves)):
        input = move(input, min_value, max_value)
    input.rotate(-input.index(1))
    return input


class LinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None


def main(input, moves=10):
    new_input = deque(map(int, list(input)))
    # part_one
    ret = perform_moves(new_input.copy(), moves)
    ret.popleft()
    print("".join(map(str, ret)))
    part_two_input = list(map(int, list(input)))
    part_two_input.extend([i for i in range(10, 10000001)])
    ret = perform_moves(deque(part_two_input), moves)
    ret.popleft()
    val_one = ret.popleft()
    val_two = ret.popleft()
    print("{} * {} = {}".format(val_one, val_two, val_one*val_two))


if __name__ == "__main__":
    main("389125467")
    main("389125467", 100)
    main("364297581", 100)
    main("389125467", 10000000)
    main("364297581", 10000000)
