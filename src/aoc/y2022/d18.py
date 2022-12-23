#!/usr/bin/env python
"""Solutions for AoC 18, 2022."""
# Created: 2022-12-18 16:19:05.738036

from collections import deque
from itertools import product

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from rich.progress import track


def parse(input_data):
    """Transform the data"""
    ret = []
    for line in input_data.splitlines():
        x, y, z = map(int, line.split(","))
        ret.append((x, y, z))
    return ret


def neighbors(x, y, z):
    yield (x - 1, y, z)
    yield (x + 1, y, z)
    yield (x, y - 1, z)
    yield (x, y + 1, z)
    yield (x, y, z - 1)
    yield (x, y, z + 1)


def get_exposed_sides(cube_coords):
    cubes = {}
    for cube in cube_coords:
        cubes[cube] = 6

    for cube in cubes:
        # *cube unpacks cube tuple
        for n in neighbors(*cube):
            if n in cubes:
                cubes[cube] -= 1
    return cubes


def solve_part_one(input_data):
    """Solve part one.

        # --- Day 18: Boiling Boulders ---
    You and the elephants finally reach fresh air. You've emerged near the
     base of a large volcano that seems to be actively erupting!
    Fortunately, the lava seems to be flowing away from you and toward the
     ocean.
    Bits of lava are still being ejected toward you, so you're sheltering
    in the cavern exit a little longer. Outside the cave, you can see the
    lava landing in a pond and hear it loudly hissing as it solidifies.
    Depending on the specific compounds in the lava and speed at which it
    cools, it might be forming
    [obsidian](https://en.wikipedia.org/wiki/Obsidian)! The cooling rate
    should be based on the surface area of the lava droplets, so you take
    a quick scan of a droplet as it flies past you (your puzzle input).
    Because of how quickly the lava is moving, the scan isn't very good;
    its resolution is quite low and, as a result, it approximates the
    shape of the lava droplet with *1x1x1 *cubes* on a 3D grid*, each
    given as its `x,y,z` position.
    To approximate the surface area, count the number of sides of each
    cube that are not immediately connected to another cube. So, if your
    scan were only two adjacent cubes like `1,1,1` and `2,1,1`, each cube
    would have a single side covered and five sides exposed, a total
    surface area of `10` sides.
    Here's a larger example:
    ```
    2,2,2
    1,2,2
    3,2,2
    2,1,2
    2,3,2
    2,2,1
    2,2,3
    2,2,4
    2,2,6
    1,2,5
    3,2,5
    2,1,5
    2,3,5
    ```
    In the above example, after counting up all the sides that aren't
    connected to another cube, the total surface area is `64`.
    *What is the surface area of your scanned lava droplet?*
    """

    # populate the cubes in cubes
    cubes = get_exposed_sides(input_data)
    answer = sum(v for _, v in cubes.items())
    return answer


def solve_part_two(input_data):
    """Solve part two.

    Something seems off about your calculation. The cooling rate depends on exterior surface area, but your calculation also included the surface area of air pockets trapped in the lava droplet.

    Instead, consider only cube sides that could be reached by the water and steam as the lava droplet tumbles into the pond. The steam will expand to reach as much as possible, completely displacing any air on the outside of the lava droplet but never expanding diagonally.

    In the larger example above, exactly one cube of air is trapped within the lava droplet (at 2,2,5), so the exterior surface area of the lava droplet is 58.

    What is the exterior surface area of your scanned lava droplet?
    """

    # From https://github.com/mebeim/aoc/blob/master/2022/README.md#day-18---boiling-boulders
    # In a 2d space:
    #   A       B       C       D
    # ..#..   .###.   #####   #####
    # .#.#.   #..#.   #...#   #.#.#
    # ..#..   #.#..   .##.#   ###.#
    #         .#...   .....   ..###
    # So we need to look around the object
    # Get a bounding box
    print("Finding external surfaces")
    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = 0

    for x, y, z in input_data:
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)
        min_z, max_z = min(min_z, z), max(max_z, z)

    # shortcut for min_x <= x <= max_x
    rangex = range(min_x, max_x + 1)
    rangey = range(min_y, max_y + 1)
    rangez = range(min_z, max_z + 1)

    cubes = get_exposed_sides(input_data)
    surfaces = sum(v for _, v in cubes.items())
    cubes = input_data

    def explore(cubes, start, rangex, rangey, rangez):
        """Use DFS to find a way out of the provided range.

        If we cannot escape, then return the number of faces we touched
        in the cubes along with where we were.
        """
        # keep track of where we've been
        seen = set()
        frontier = deque([start])
        faces_touched = 0

        while frontier:
            point = frontier.pop()
            if point in seen:
                continue

            seen.add(point)
            x, y, z = point

            if not (x in rangex and y in rangey and z in rangez):
                # we've escaped!
                return 0, seen

            # We're inside the bounding box
            for n in neighbors(x, y, z):
                # Did we hit a cube?
                if n in cubes:
                    # Add to the faces touched
                    faces_touched += 1
                else:
                    # otherwise, check out the neighbor
                    if n not in seen:
                        frontier.append(n)
        return faces_touched, seen

    all_seen = set()

    # Now we can actually check all starting points
    for point in track(
        product(rangex, rangey, rangez), description="Exploring the space"
    ):
        if point in cubes or point in all_seen:
            continue
        faces_touched, seen = explore(cubes, point, rangex, rangey, rangez)
        # remove the internal faces that we touched from all surfaces
        surfaces -= faces_touched
        # extend seen with more points
        all_seen |= seen

    print(f"Found {surfaces}")
    answer = surfaces
    return answer


def main():
    puzzle = Puzzle(year=2022, day=18)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2022).get((2022, 18), {})
    if stats.get("a", None) is None:
        print("Solving part 1")
        answer_a = solve_part_one(parsed_data)
        if answer_a:
            puzzle.answer_a = answer_a
    if stats.get("b", None) is None:
        print("Solving part 2")
        parsed_data = parse(puzzle.input_data)
        answer_b = solve_part_two(parsed_data)
        if answer_b:
            puzzle.answer_b = answer_b


if __name__ == "__main__":
    main()
