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


@pytest.mark.parametrize(
    "input, expected",
    [
        ([0, 2, 5, 8, 6, 4, 7, 3, 9, 1], [0, 5, 8, 2, 6, 4, 7, 3, 9, 1]),
    ],
)
def test_perform_moves(input, expected):
    assert perform_moves(input, 1, 3) == expected


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


def perform_moves(input, moves, current_label):
    max_value = max(input)
    for _ in tqdm.tqdm(range(moves)):
    # for _ in range(moves):
        first = input[current_label]
        mid = input[first]
        last = input[mid]

        # update current label next to the one after the last picked up
        input[current_label] = input[last]

        # get the destination value
        # insert_value = current_label - 1
        # if insert_value == 1:
        #     insert_value = max_value
        dst = max_value if current_label == 1 else current_label - 1

        while dst in (first, mid, last):
            dst = max_value if dst == 1 else dst - 1

        # update last picked up next value
        input[last] = input[dst]
        # update insert next value to the first picked up
        input[dst] = first

        current_label = input[current_label]
    return input


@pytest.mark.parametrize(
    "input, max_value, expected",
    [
        ("389125467", None, [0, 2, 5, 8, 6, 4, 7, 3, 9, 1]),
        ("389125467", 10, [0, 2, 5, 8, 6, 4, 7, 10, 9, 1, 3]),
        ("389125467", 11, [0, 2, 5, 8, 6, 4, 7, 10, 9, 1, 11, 3]),
    ],
)
def test_transform_input(input, max_value, expected):
    new_input = transform_input(input, max_value)
    assert new_input == expected


def transform_input(input, max_value=None):
    # # Convert input to list of ints
    cups = list(map(int, list(input)))
    # current_label = input[0]
    # # shift everything one index right
    # new_input = [0] * (len(input))
    # # Use zip to combine the current input with the input shifted 1
    # for prev, cur in zip(input, input[1:]):
    #     new_input[prev] = cur

    # if max_value is not None:
    #     # new_input.extend([i for i in range(len(input) + 1, max_value + 1)])
    #     new_input.extend(list(range(len(input) + 1, max_value + 1)))
    # # Add the loop around value
    #     new_input[-1] = current_label
    #     new_input[input[-1]] = len(input)+1
    # else:
    #     new_input[input[-1]] = current_label
    # return new_input
    next_cup = [0] * (len(cups)+1)
    n = max_value

    for prev, cur in zip(cups, cups[1:]):
        next_cup[prev] = cur

    if n is not None:
        next_cup += list(range(len(cups) + 2, n + 1))
        next_cup.append(cups[0])
        next_cup[cups[-1]] = len(cups) + 1
    else:
        next_cup[cups[-1]] = cups[0]
    return next_cup


def main(input, moves=10):
    input = list(map(int, list(input)))
    current_label = input[0]
    # shift everything one index right
    new_input = transform_input(input)
    ret = perform_moves(new_input, moves, current_label)
    ans = ''
    cur = ret[1]
    while cur != 1:
        ans += str(cur)
        cur = ret[cur]

    print('Part 1:', ans)
    new_input = transform_input(input, max_value=1000000)
    ret = perform_moves(new_input, moves=moves, current_label=current_label)
    val_one = ret[1]
    val_two = ret[val_one]
    print("Part 2:", val_one*val_two)


if __name__ == "__main__":
    # main("389125467")
    main("389125467", 100)
    # main("364297581", 100)
    main("389125467", 10000000)
    main("364297581", 10000000)
