#!/usr/bin/env python
"""Solutions for AoC 10, 2023."""
# Created: 2023-12-10 12:12:30.481738

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from collections import namedtuple, defaultdict


CardinalDirection = namedtuple("CardinalDirection", ["delta_x", "delta_y"])

# Lookups for how to change the coordinate
North = (0, -1)  # I have to inverse north because y goes down in my parsing
South = (0, 1)  # I have to inverse south because y goes down in my parsing
East = (1, 0)
West = (-1, 0)
Ground = (0, 0)
# Lookup for cardinal directions
Pipes = {
    "|": (North, South),
    "-": (East, West),
    "L": (North, East),
    "J": (North, West),
    "7": (South, West),
    "F": (South, East),
    ".": (Ground, Ground),
}


def parse(input_data):
    """Transform the data

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the
      pipe has.

    Returns a default dictionary with each value being the character of the coordinate
    """
    parsed_data = defaultdict(lambda: ".")
    for y, row in enumerate(input_data.splitlines()):
        for x, value in enumerate(row):
            parsed_data[(x, y)] = value
    return parsed_data


map_neighbors = None


def get_map_neighbors(map_data):
    """Precalculate all neighbors"""
    neighbors = {}
    global map_neighbors
    if map_neighbors:
        return map_neighbors
    nodes_to_consider = map_data.items()

    for coordinate, value in nodes_to_consider:
        left, right = Pipes[value]

        left_neighbor = (left[0] + coordinate[0], left[1] + coordinate[1])
        right_neighbor = (right[0] + coordinate[0], right[1] + coordinate[1])
        neighbors[coordinate] = (left_neighbor, right_neighbor)
    map_neighbors = neighbors
    return neighbors


def get_start_pipe(map_data, start_coordinate):
    """Figure out what character the start coordinate should be.

    According to the instructions, I can determine what the start coordinate pipe is based on the pipes around it.

    In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect
    to it.
    """
    directions = [
        (0, 1),  # south
        (1, 0),  # east
        (0, -1),  # nouth
        (-1, 0),  # west
    ]
    x, y = start_coordinate
    found_neighbors = []
    for direction in directions:
        new_x, new_y = x + direction[0], y + direction[1]
        neighbor_pipe = map_data[(new_x, new_y)]
        pipe_directions = Pipes[neighbor_pipe]
        if new_x + pipe_directions[0][0] == x and new_y + pipe_directions[0][1] == y:
            found_neighbors.append(direction)
        if new_x + pipe_directions[1][0] == x and new_y + pipe_directions[1][1] == y:
            found_neighbors.append(direction)
    assert len(found_neighbors) == 2
    for pipe_character in Pipes:
        if set(Pipes[pipe_character]) == set(found_neighbors):
            return pipe_character
    raise ValueError


def get_pipe(input_data, coordinates):
    """Given a coordinate, determine what pipe it has."""
    x, y = coordinates
    value = input_data[(x, y)]
    if value != "S":
        return value


def get_next_node(map_data, coordinate, previous_coordinate):
    """Find the next node.

    The next node can by found by eliminating the previous coordinate from the available coordinates for the current
    coordinate
    """
    # map_data[coordinate] returns a character
    # directions returns a set of cardinal directions
    directions = Pipes[map_data[coordinate]]
    # print(f"{previous_coordinate} {map_data[coordinate]}")

    assert directions != (Ground, Ground)
    left_coordinate = (
        coordinate[0] + directions[0][0],
        coordinate[1] + directions[0][1],
    )
    right_coordinate = (
        coordinate[0] + directions[1][0],
        coordinate[1] + directions[1][1],
    )
    if previous_coordinate == left_coordinate:
        # print(
        #     f"{map_data[coordinate]}: {left_coordinate} - ({coordinate}) -> {right_coordinate}"
        # )
        return right_coordinate, coordinate
    if previous_coordinate == right_coordinate:
        # print(
        #     f"{map_data[coordinate]}: {right_coordinate} - ({coordinate}) -> {left_coordinate}"
        # )
        return left_coordinate, coordinate
    # print(
    #     f"{map_data[coordinate]}: {left_coordinate} ? {right_coordinate} != {previous_coordinate}"
    # )
    raise ValueError


def solve_part_one(input_data, start_coordinate=None):
    """Solve part one.

    Take in a start coordinate because the S isn't in the example data"""
    answer = 0
    # get the start coordinate
    for coordinate, pipe in input_data.items():
        if pipe == "S":
            start_coordinate = coordinate
            break
    else:
        if not start_coordinate:
            print("Could not find a start coordinate")
            print(input_data)
            raise ValueError

    input_data[start_coordinate] = get_start_pipe(input_data, start_coordinate)
    neighbors = get_map_neighbors(input_data)
    # walk both directions along the loop
    iters = 1
    max_iters = 10**5
    left_node, right_node = neighbors[start_coordinate]
    print(neighbors[start_coordinate])
    previous_left_node, previous_right_node = start_coordinate, start_coordinate
    # I can traverse both directions from start until they meet
    while iters < max_iters:
        iters += 1
        left_node, previous_left_node = get_next_node(
            input_data, left_node, previous_left_node
        )
        right_node, previous_right_node = get_next_node(
            input_data, right_node, previous_right_node
        )

        if left_node == right_node:
            break
    answer = iters
    return answer


def solve_part_two(input_data):
    """Solve part two."""
    answer = None
    return answer


def main():
    puzzle = Puzzle(year=2023, day=10)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 10), {})
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
