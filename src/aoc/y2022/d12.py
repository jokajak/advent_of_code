#!/usr/bin/env python
"""Solutions for AoC 12, 2022."""
# Created: 2022-12-12 08:39:08.648263

import string
from collections import defaultdict
from typing import Iterator

# Standard library imports
from aocd.models import Puzzle

from aoc.utils import pathfinding
from aoc.utils.pathfinding import (
    GridLocation,
    a_star_search,
    dijkstra_search,
    draw_grid,
    reconstruct_path,
)


class Hill(pathfinding.GridWithWeights):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.nodes: dict[GridLocation, str] = {}
        self.weights: dict[GridLocation, dict[GridLocation]] = defaultdict(dict)
        self.reversed = False

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> int:
        from_node_letter = self.nodes[from_node]
        to_node_letter = self.nodes[to_node]
        # print(f"{from_node} ({from_node_letter}) {to_node} ({to_node_letter})")
        cost = string.ascii_letters.index(to_node_letter) - string.ascii_letters.index(
            from_node_letter
        )
        if cost > 1:
            # print("Shouldn't get here")
            return self.width * self.height * 9999
        else:
            return cost + 1

    def draw(self, trim=True):
        draw_grid(self, letter=self.nodes, trim=trim, start=self.start, goal=self.goal)

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0:
            neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        r = []
        node_letter = self.nodes[id]
        for entry in results:
            neighbor_letter = self.nodes[entry]
            # print(f"{id} {node_letter} {neighbor_letter} {entry}")
            if (
                string.ascii_letters.index(neighbor_letter)
                - string.ascii_letters.index(node_letter)
            ) > 1:
                continue
            r.append(entry)
        return r


def parse(input_data):
    """Transform the data"""
    input_data = input_data.splitlines()
    grid = Hill(width=len(input_data[0]), height=len(input_data))
    # Convert string to grid
    for col_index, line in enumerate(input_data):
        for row_index, c in enumerate(line):
            if c == "S":
                grid.start = (row_index, col_index)
                c = "a"
            elif c == "E":
                grid.goal = (row_index, col_index)
                c = "z"
            grid.nodes[(row_index, col_index)] = c
    return grid


def solve_part_one(input_data):
    """Solve part one.

        # --- Day 12: Hill Climbing Algorithm ---
    You try contacting the Elves using your *handheld device*, but the
    river you're following must be too low to get a decent signal.
    You ask the device for a heightmap of the surrounding area (your
    puzzle input). The heightmap shows the local area from above broken
    into a grid; the elevation of each square of the grid is given by a
    single lowercase letter, where `a` is the lowest elevation, `b` is the
     next-lowest, and so on up to the highest elevation, `z`.
    Also included on the heightmap are marks for your current position
    (`S`) and the location that should get the best signal (`E`). Your
    current position (`S`) has elevation `a`, and the location that should
     get the best signal (`E`) has elevation `z`.
    You'd like to reach `E`, but to save energy, you should do it in *as
    few steps as possible*. During each step, you can move exactly one
    square up, down, left, or right. To avoid needing to get out your
    climbing gear, the elevation of the destination square can be *at most
     one higher* than the elevation of your current square; that is, if
    your current elevation is `m`, you could step to elevation `n`, but
    not to elevation `o`. (This also means that the elevation of the
    destination square can be much lower than the elevation of your
    current square.)
    For example:
    ```
    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi
    ```
    Here, you start in the top-left corner; your goal is near the middle.
    You could start by moving down or right, but eventually you'll need to
     head toward the `e` at the bottom. From there, you can spiral around
    to the goal:
    ```
    v..v<<<<
    >v.vv<<^
    .>vv>E^^
    ..v>>>^^
    ..>>>>>^
    ```
    In the above diagram, the symbols indicate whether the path exits each
     square moving up (`^`), down (`v`), left (`<`), or right (`>`). The
    location that should get the best signal is still `E`, and `.` marks
    unvisited squares.
    This path reaches the goal in `31` steps, the fewest possible.
    *What is the fewest steps required to move from your current position
    to the location that should get the best signal?*
    """
    hill = input_data
    # hill.draw()
    came_from, cost_so_far = a_star_search(hill, hill.start, hill.goal)
    came_from, cost_so_far = dijkstra_search(hill, hill.start, hill.goal)
    (hill, hill.start, hill.goal)
    # draw_grid(hill, point_to=came_from, start=hill.start, goal=hill.goal, trim=True)
    # print()
    # draw_grid(
    #     hill,
    #     path=reconstruct_path(
    #         came_from, start=hill.start, goal=hill.goal, reverse=True
    #     ),
    #     start=hill.start,
    #     goal=hill.goal,
    #     trim=False,
    # )
    pathlen = reconstruct_path(
        came_from, start=hill.start, goal=hill.goal, add_start=False
    )
    answer = len(pathlen)
    return answer


def solve_part_two(input_data):
    """Solve part two.

    As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

    To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

    Again consider the example from above:

    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi

    Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

    ...v<<<<
    ...vv<<^
    ...v>E^^
    .>v>>>^^
    >^>>>>>^

    This path reaches the goal in only 29 steps, the fewest possible.

    What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?
    """
    hill = input_data
    hill.draw(trim=True)
    r = "c"

    start_options = []
    for node, char in hill.nodes.items():
        if char == "a":
            start_options.append(node)
    min_len = float("inf")
    assert hill.start in start_options
    for pos in start_options:
        if r != "c":
            r = input("Continue? ")

        start = pos
        goal = hill.goal
        path, costs = a_star_search(hill, start, goal)
        path_cost = len(
            reconstruct_path(
                path,
                goal=goal,
                start=start,
                add_start=False,
            )
        )
        if path_cost == 0:
            continue
        draw_grid(
            hill,
            path=reconstruct_path(path, start=start, goal=goal, reverse=True),
            start=hill.start,
            goal=hill.goal,
            trim=True,
        )
        min_len = min(path_cost, min_len)
    answer = min_len
    return answer


def main():
    puzzle = Puzzle(year=2022, day=12)
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
