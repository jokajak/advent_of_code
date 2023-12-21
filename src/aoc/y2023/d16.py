#!/usr/bin/env python
"""Solutions for AoC 16, 2023."""
# Created: 2023-12-18 22:00:08.851960

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from collections import deque


class Graph:
    def __init__(self, graph, height, width):
        self.graph = graph
        self.height = height
        self.width = width

    def print_visited(self, visited_coords):
        """Print the graph with visited coordinates displayed"""
        for y in range(self.height):
            line = []
            for x in range(self.width):
                if (x, y) in visited_coords:
                    line.append("#")
                else:
                    line.append(self.graph[(x, y)])
            print("".join(line))


def parse(input_data):
    """Transform the data"""
    parsed_data = {}
    height = len(input_data.splitlines())
    width = len(input_data.splitlines()[0])
    for y, row in enumerate(input_data.splitlines()):
        for x, value in enumerate(row):
            parsed_data[(x, y)] = value
    return Graph(parsed_data, height, width)


def shoot_laser(graph, start_coordinate, direction):
    """Collect the list of coordinates that a laser touches.

    If a laser hits a split then it stops and new lasers come out.

    This way, a laser can only visit a node once

    Returns:
    * a set of visited nodes
    * a list of rays
    """
    max_path_length = 10**100
    x, y = start_coordinate
    visited_coords = {}
    delta_x, delta_y = direction
    height, width = graph.height, graph.width
    graph = graph.graph
    for _ in range(max_path_length):
        next_x = x + delta_x
        next_y = y + delta_y
        next_coord = (next_x, next_y)
        if next_x < 0 or next_y < 0 or next_x >= width or next_y >= height:
            # We reached the edge of the graph
            return visited_coords, []
        visited_coords[(next_coord)] = True
        if graph[(next_coord)] == "|" and delta_x != 0:
            # this ray is splitting
            return visited_coords, [(next_coord, (0, 1)), (next_coord, (0, -1))]
        if graph[(next_coord)] == "-" and delta_y != 0:
            # this ray is splitting
            return visited_coords, [(next_coord, (-1, 0)), (next_coord, (1, 0))]
        if graph[(next_coord)] == "/":
            # the ray turns
            if delta_y == 0:
                delta_y = -delta_x
                delta_x = 0
            else:
                delta_x = -delta_y
                delta_y = 0
            # if delta_x == 1:
            #     # turn up
            #     delta_x = 0
            #     delta_y = 1
            # if delta_x == -1:
            #     # turn down
            #     delta_x = 0
            #     delta_y = -1
        if graph[(next_coord)] == "\\":
            # the ray turns
            if delta_y == 0:
                delta_y = delta_x
                delta_x = 0
            else:
                delta_x = delta_y
                delta_y = 0
        x, y = next_x, next_y
    raise ValueError


def energize_tiles(start_coordinate, direction, graph):
    # each ray is a coordinate and a direction
    rays = [(start_coordinate, direction)]
    # I need to keep track of the visited coordinates
    visited_coords = {}
    # I need to keep track of launched rays so I don't shoot them again
    launched_rays = {}
    # simple loop limiter
    max_iters = 10 * 100
    for i in range(max_iters):
        # print(f"({i}) Rays: {len(rays)}")
        coord, direction = rays.pop()
        ray_coords, new_rays = shoot_laser(graph, coord, direction)
        visited_coords.update(ray_coords)
        for ray in new_rays:
            if ray not in launched_rays:
                launched_rays[ray] = True
                rays.append(ray)
        if not rays:
            break
    return visited_coords


def solve_part_one(input_data):
    """Solve part one."""
    visited_coords = energize_tiles((-1, 0), (1, 0), input_data)
    input_data.print_visited(visited_coords)
    answer = len(visited_coords)
    return answer


def solve_part_two(input_data):
    """Solve part two.

    Determine the best starting coordinate to maximize the most tiles.
    """
    answer = 0
    # to shoot the laser, it starts at either:
    # x=-1, y = 0-height, direction = (1, 0)
    for y in range(input_data.height):
        visited_coords = energize_tiles((-1, y), (1, 0), input_data)
        answer = max(answer, len(visited_coords))
    # y = -1, x = 0-width, direction = (0, 1)
    for x in range(input_data.width):
        visited_coords = energize_tiles((x, -1), (0, 1), input_data)
        answer = max(answer, len(visited_coords))
    # x=width, y = 0-height, direction = (-1, 0)
    for y in range(input_data.height):
        visited_coords = energize_tiles((input_data.width, y), (-1, 0), input_data)
        answer = max(answer, len(visited_coords))
    # y = height, x = 0-width, direction = (0, -1)
    for x in range(input_data.width):
        visited_coords = energize_tiles((x, input_data.height), (0, -1), input_data)
        answer = max(answer, len(visited_coords))
    return answer


def main():
    puzzle = Puzzle(year=2023, day=16)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 16), {})
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
