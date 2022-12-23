#!/usr/bin/env python
"""Solutions for AoC 17, 2022."""
# Created: 2022-12-18 16:19:11.371754

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import inspect, print


def parse(input_data):
    """Transform the data"""
    # >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
    mapping = {">": 1, "<": -1}
    ret = []
    for c in input_data:
        ret.append(mapping[c])
    return ret


class Rock:
    def __init__(self, rock):
        self.rock = rock
        self.width = max(len(r) for r in rock)
        self.height = len(rock)


# fmt: off
ROCKS = [
    [[2, 2, 2, 2]],
    [
        [0, 2, 0],
        [2, 2, 2],
        [0, 2, 0],
    ],
    [
        [0, 0, 2],
        [0, 0, 2],
        [2, 2, 2],
    ],
    [
        [2],
        [2],
        [2],
        [2],
    ],
    [
        [2, 2],
        [2, 2],
    ],
]
# fmt: on
ROCKS = [Rock(reversed(r)) for r in ROCKS]


def solve_part_one(input_data):
    """Solve part one.

        # --- Day 17: Pyroclastic Flow ---
    Your handheld device has located an alternative exit from the cave for
     you and the elephants.  The ground is rumbling almost continuously
    now, but the strange valves bought you some time. It's definitely
    getting warmer in here, though.
    The tunnels eventually open into a very tall, narrow chamber. Large,
    oddly-shaped rocks are falling into the chamber from above, presumably
     due to all the rumbling. If you can't work out where the rocks will
    fall next, you might be *crushed*!
    The five types of rocks have the following peculiar shapes, where `#`
    is rock and `.` is empty space:
    ```
    ####
    .#.
    ###
    .#.
    ..#
    ..#
    ###
    #
    #
    #
    #
    ##
    ##
    ```
    The rocks fall in the order shown above: first the `-` shape, then the
     `+` shape, and so on. Once the end of the list is reached, the same
    order repeats: the `-` shape falls first, sixth, 11th, 16th, etc.
    The rocks don't spin, but they do get pushed around by jets of hot gas
     coming out of the walls themselves. A quick scan reveals the effect
    the jets of hot gas will have on the rocks as they fall (your puzzle
    input).
    For example, suppose this was the jet pattern in your cave:
    ```
    >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
    ```
    In jet patterns, `<` means a push to the left, while `>` means a push
    to the right. The pattern above means that the jets will push a
    falling rock right, then right, then right, then left, then left, then
     right, and so on. If the end of the list is reached, it repeats.
    The tall, vertical chamber is exactly *seven units wide*. Each rock
    appears so that its left edge is two units away from the left wall and
     its bottom edge is three units above the highest rock in the room (or
     the floor, if there isn't one).
    After a rock appears, it alternates between *being pushed by a jet of
    hot gas* one unit (in the direction indicated by the next symbol in
    the jet pattern) and then *falling one unit down*. If any movement
    would cause any part of the rock to move into the walls, floor, or a
    stopped rock, the movement instead does not occur. If a *downward*
    movement would have caused a falling rock to move into the floor or an
     already-fallen rock, the falling rock stops where it is (having
    landed on something) and a new rock immediately begins falling.
    Drawing falling rocks with `@` and stopped rocks with `#`, the jet
    pattern in the example above manifests as follows:
    ```
    The first rock begins falling:
    |..@@@@.|
    |.......|
    |.......|
    |.......|
    +-------+
    Jet of gas pushes rock right:
    |...@@@@|
    |.......|
    |.......|
    |.......|
    +-------+
    Rock falls 1 unit:
    |...@@@@|
    |.......|
    |.......|
    +-------+
    Jet of gas pushes rock right, but nothing happens:
    |...@@@@|
    |.......|
    |.......|
    +-------+
    Rock falls 1 unit:
    |...@@@@|
    |.......|
    +-------+
    Jet of gas pushes rock right, but nothing happens:
    |...@@@@|
    |.......|
    +-------+
    Rock falls 1 unit:
    |...@@@@|
    +-------+
    Jet of gas pushes rock left:
    |..@@@@.|
    +-------+
    Rock falls 1 unit, causing it to come to rest:
    |..####.|
    +-------+
    A new rock begins falling:
    |...@...|
    |..@@@..|
    |...@...|
    |.......|
    |.......|
    |.......|
    |..####.|
    +-------+
    Jet of gas pushes rock left:
    |..@....|
    |.@@@...|
    |..@....|
    |.......|
    |.......|
    |.......|
    |..####.|
    +-------+
    Rock falls 1 unit:
    |..@....|
    |.@@@...|
    |..@....|
    |.......|
    |.......|
    |..####.|
    +-------+
    Jet of gas pushes rock right:
    |...@...|
    |..@@@..|
    |...@...|
    |.......|
    |.......|
    |..####.|
    +-------+
    Rock falls 1 unit:
    |...@...|
    |..@@@..|
    |...@...|
    |.......|
    |..####.|
    +-------+
    Jet of gas pushes rock left:
    |..@....|
    |.@@@...|
    |..@....|
    |.......|
    |..####.|
    +-------+
    Rock falls 1 unit:
    |..@....|
    |.@@@...|
    |..@....|
    |..####.|
    +-------+
    Jet of gas pushes rock right:
    |...@...|
    |..@@@..|
    |...@...|
    |..####.|
    +-------+
    Rock falls 1 unit, causing it to come to rest:
    |...#...|
    |..###..|
    |...#...|
    |..####.|
    +-------+
    A new rock begins falling:
    |....@..|
    |....@..|
    |..@@@..|
    |.......|
    |.......|
    |.......|
    |...#...|
    |..###..|
    |...#...|
    |..####.|
    +-------+
    ```
    The moment each of the next few rocks begins falling, you would see
    this:
    ```
    |..@....|
    |..@....|
    |..@....|
    |..@....|
    |.......|
    |.......|
    |.......|
    |..#....|
    |..#....|
    |####...|
    |..###..|
    |...#...|
    |..####.|
    +-------+
    |..@@...|
    |..@@...|
    |.......|
    |.......|
    |.......|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+
    |..@@@@.|
    |.......|
    |.......|
    |.......|
    |....##.|
    |....##.|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+
    |...@...|
    |..@@@..|
    |...@...|
    |.......|
    |.......|
    |.......|
    |.####..|
    |....##.|
    |....##.|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+
    |....@..|
    |....@..|
    |..@@@..|
    |.......|
    |.......|
    |.......|
    |..#....|
    |.###...|
    |..#....|
    |.####..|
    |....##.|
    |....##.|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+
    |..@....|
    |..@....|
    |..@....|
    |..@....|
    |.......|
    |.......|
    |.......|
    |.....#.|
    |.....#.|
    |..####.|
    |.###...|
    |..#....|
    |.####..|
    |....##.|
    |....##.|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+
    |..@@...|
    |..@@...|
    |.......|
    |.......|
    |.......|
    |....#..|
    |....#..|
    |....##.|
    |....##.|
    |..####.|
    |.###...|
    |..#....|
    |.####..|
    |....##.|
    |....##.|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+
    |..@@@@.|
    |.......|
    |.......|
    |.......|
    |....#..|
    |....#..|
    |....##.|
    |##..##.|
    |######.|
    |.###...|
    |..#....|
    |.####..|
    |....##.|
    |....##.|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+
    ```
    To prove to the elephants your simulation is accurate, they want to
    know how tall the tower will get after 2022 rocks have stopped (but
    before the 2023rd rock begins falling). In this example, the tower of
    rocks will be `3068` units tall.
    *How many units tall will the tower of rocks be after 2022 rocks have
    stopped falling?*
    """
    # The tall, vertical chamber is exactly *seven units wide*. Each rock
    # appears so that its left edge is two units away from the left wall and
    #  its bottom edge is three units above the highest rock in the room (or
    #  the floor, if there isn't one).

    answer = drop_rocks(jets=input_data, rock_count=2022)
    return answer


def draw_tile(chamber, y, x):
    r = "."
    if y == 0:
        if x == -1 or x > len(chamber[y]):
            r = "+"
        else:
            r = "-"
    else:
        if x == -1 or x > len(chamber[y]):
            r = "|"
        elif chamber[y][x] == 1:
            r = "#"
        elif chamber[y][x] == 2:
            r = "@"
    return r


def print_chamber(chamber):
    for y in range(len(chamber) - 1, -1, -1):
        print(f"{draw_tile(chamber, y, -1)}", end="")
        for x in range(len(chamber[y])):
            print(f"{draw_tile(chamber, y, x)}", end="")
        print(f"{draw_tile(chamber, y, 9)}")


def drop_rocks(jets, rock_count=2022):
    # The tall, vertical chamber is exactly *seven units wide*. Each rock
    # appears so that its left edge is two units away from the left wall and
    #  its bottom edge is three units above the highest rock in the room (or
    #  the floor, if there isn't one).
    # Invert the chamber so y goes up
    chamber = [
        [1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    print_chamber(chamber)
    for counter in range(rock_count + 1):
        rock = ROCKS[counter % len(ROCKS)]
        delta = jets[counter % len(jets)]
        left, right = 2, 2 + rock.width
        bottom, top = rock.height, rock.height + 2
        # The above is naive and dumb
        # after a rock appears, it alternates between *being pushed by a jet of
        # hot gas* one unit (in the direction indicated by the next symbol in
        # the jet pattern) and then *falling one unit down*. if any movement
        # stopped rock, the movement instead does not occur. If a *downward*
        # movement would have caused a falling rock to move into the floor or an
        #  already-fallen rock, the falling rock stops where it is (having
        # landed on something) and a new rock immediately begins falling.
        # Drawing falling rocks with `@` and stopped rocks with `#`, the jet
        # pattern in the example above manifests as follows:
        # A rock will fall down only a few places, depending on the jets and
        # would cause any part of the rock to move into the walls, floor, or a
        # the contour of the chamber

    pass


def solve_part_two(input_data):
    """Solve part two."""
    answer = None
    return answer


def main():
    puzzle = Puzzle(year=2022, day=17)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2022).get((2022, 17), {})
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
