#!/usr/bin/env python
"""Solutions for AoC 14, 2022."""
# Created: 2022-12-14 09:53:25.343977

from typing import Iterable

# Standard library imports
from aocd.models import Puzzle
from rich.progress import track

from aoc.utils import pathfinding


class Cave(pathfinding.SquareGrid):
    def __init__(self, paths, bottomless: bool = True):
        self.sand_start = (500, 0)
        self.walls: list[pathfinding.GridLocation] = []
        self.sand: list[pathfinding.GridLocation] = []
        self.bottom = None

        walls = []
        min_x, min_y, max_x, max_y = float("inf"), float("inf"), 0, 0
        # follow 498,4 -> 498,6 -> 496,6
        # such that (498,4), (498, 5), (498, 6), (497, 6), (496, 6) are '#'
        for path in paths:
            for point in Cave.parse_path(path):
                col, row = point
                min_x, min_y = min(row, min_x), min(col, min_y)
                max_x, max_y = max(row, max_x), max(col, max_y)
                walls.append(point)

        # scale wall points down
        for row, col in walls:
            self.walls.append((col - min_x, row))
        self.width = abs(min_x - max_x) + 2
        self.height = max_y
        self.sand_start = (500 - min_x, 0)

    def add_bottom(self, row: int):
        """Add a bottom to the cave."""
        # y = mx + b
        # sand_start = (500 - min_x, 0)
        # y = x - (500 - min_x)
        # bottom = x - (500 - min_x)
        # x = bottom + (500 - min_x)
        self.bottom = row

    def in_bounds(self, id: pathfinding.GridLocation) -> bool:
        (x, y) = id
        if self.bottom:
            return y <= self.bottom
        else:
            return 0 <= x <= self.width and 0 <= y <= self.height

    @staticmethod
    def parse_path(path: str) -> Iterable:
        """Parse a string of path points.

        follow 498,4 -> 498,6 -> 496,6
        such that (498,4), (498, 5), (498, 6), (497, 6), (496, 6) are '#'

        return a list of points
        """
        path_points = path.split(" -> ")

        points = {}
        prev_point = None
        for point in path_points:
            y, x = point.split(",")
            x, y = int(x), int(y)
            if not prev_point:
                prev_point = (x, y)
                continue
            prev_x, prev_y = prev_point
            # Make sure we're not on a diagonal
            prev_point = (x, y)
            for x_pos in range(min(x, prev_x), max(x, prev_x) + 1):
                for y_pos in range(min(y, prev_y), max(y, prev_y) + 1):
                    points[(x_pos, y_pos)] = True
        return points.keys()

    def draw(self):
        pathfinding.draw_grid(
            self, y_min=0, x_min=-5, sand=self.sand, trim=True, start=self.sand_start
        )

    def add_sand(self) -> bool:
        """Add sand to the grid.

        Sand is produced *one unit at a time*, and the next unit of sand is
        not produced until the previous unit of sand *comes to rest*. A unit
        of sand is large enough to fill one tile of air in your scan.
        A unit of sand always falls *down one step* if possible. If the tile
        immediately below is blocked (by rock or sand), the unit of sand
        attempts to instead move diagonally *one step down and to the left*.
        If that tile is blocked, the unit of sand attempts to instead move
        diagonally *one step down and to the right*. Sand keeps moving as long
         as it is able to do so, at each step trying to move down, then down-
        left, then down-right. If all three possible destinations are blocked,
         the unit of sand *comes to rest* and no longer moves, at which point
        the next unit of sand is created back at the source.

        Return True if sand was stopped
        """
        col, row = self.sand_start
        next_positions = (
            (0, 1),
            (-1, 1),
            (1, 1),
        )
        # Don't run for too long
        max_positions = 100000
        for i in range(max_positions):
            if not self.passable((col, row)):
                return False
            for pos_delta in next_positions:
                delta_col, delta_row = pos_delta
                if self.passable((col + delta_col, row + delta_row)):
                    col = col + delta_col
                    row = row + delta_row
                    break  # break from inner loop because we can keep going
                # finished for loop, coludn't move the sand
            else:
                self.sand.append((col, row))
                return True
            if not self.in_bounds((col, row)):
                if self.bottom:
                    self.sand.append((col, row))
                    return True
                else:
                    return False
        else:
            raise ValueError("Sand didn't settle.")

    def passable(self, id: pathfinding.GridLocation) -> bool:
        return id not in self.walls and id not in self.sand


def parse(input_data):
    """Transform the data"""
    lines = input_data.splitlines()
    graph = Cave(lines)
    return graph


def solve_part_one(input_data):
    """Solve part one.

        # --- Day 14: Regolith Reservoir ---
    The distress signal leads you to a giant waterfall! Actually, hang on
    - the signal seems like it's coming from the waterfall itself, and
    that doesn't make any sense. However, you do notice a little path that
     leads *behind* the waterfall.
    Correction: the distress signal leads you behind a giant waterfall!
    There seems to be a large cave system here, and the signal definitely
    leads further inside.
    As you begin to make your way deeper underground, you feel the ground
    rumble for a moment. Sand begins pouring into the cave! If you don't
    quickly figure out where the sand is going, you could quickly become
    trapped!
    Fortunately, your [familiarity](/2018/day/17) with analyzing the path
    of falling material will come in handy here. You scan a two-
    dimensional vertical slice of the cave above you (your puzzle input)
    and discover that it is mostly *air* with structures made of *rock*.
    Your scan traces the path of each solid rock structure and reports the
     `x,y` coordinates that form the shape of the path, where `x`
    represents distance to the right and `y` represents distance down.
    Each path appears as a single line of text in your scan. After the
    first point of each path, each point indicates the end of a straight
    horizontal or vertical line to be drawn from the previous point. For
    example:
    ```
    498,4 -> 498,6 -> 496,6
    503,4 -> 502,4 -> 502,9 -> 494,9
    ```
    This scan means that there are two paths of rock; the first path
    consists of two straight lines, and the second path consists of three
    straight lines. (Specifically, the first path consists of a line of
    rock from `498,4` through `498,6` and another line of rock from
    `498,6` through `496,6`.)
    The sand is pouring into the cave from point `500,0`.
    Drawing rock as `#`, air as `.`, and the source of the sand as `+`,
    this becomes:
    ```
      4     5  5
      9     0  0
      4     0  3
    0 ......+...
    1 ..........
    2 ..........
    3 ..........
    4 ....#...##
    5 ....#...#.
    6 ..###...#.
    7 ........#.
    8 ........#.
    9 #########.
    ```
    Sand is produced *one unit at a time*, and the next unit of sand is
    not produced until the previous unit of sand *comes to rest*. A unit
    of sand is large enough to fill one tile of air in your scan.
    A unit of sand always falls *down one step* if possible. If the tile
    immediately below is blocked (by rock or sand), the unit of sand
    attempts to instead move diagonally *one step down and to the left*.
    If that tile is blocked, the unit of sand attempts to instead move
    diagonally *one step down and to the right*. Sand keeps moving as long
     as it is able to do so, at each step trying to move down, then down-
    left, then down-right. If all three possible destinations are blocked,
     the unit of sand *comes to rest* and no longer moves, at which point
    the next unit of sand is created back at the source.
    So, drawing sand that has come to rest as `o`, the first unit of sand
    simply falls straight down and then stops:
    ```
    ......+...
    ..........
    ..........
    ..........
    ....#...##
    ....#...#.
    ..###...#.
    ........#.
    ......o.#.
    #########.
    ```
    The second unit of sand then falls straight down, lands on the first
    one, and then comes to rest to its left:
    ```
    ......+...
    ..........
    ..........
    ..........
    ....#...##
    if trim:
    ....#...#.
    ..###...#.
    ........#.
    .....oo.#.
    #########.
    ```
    After a total of five units of sand have come to rest, they form this
    pattern:
    ```
    ......+...
    ..........
    ..........
    ..........
    ....#...##
    ....#...#.
    ..###...#.
    ......o.#.
    ....oooo#.
    #########.
    ```
    After a total of 22 units of sand:
    ```
    ......+...
    ..........
    ......o...
    .....ooo..
    ....#ooo##
    ....#ooo#.
    ..###ooo#.
    ....oooo#.
    ...ooooo#.
    #########.
    ```
    Finally, only two more units of sand can possibly come to rest:
    ```
    ......+...
    ..........
    ......o...
    .....ooo..
    ....#ooo##
    ...o#ooo#.
    ..###ooo#.
    ....oooo#.
    .o.ooooo#.
    #########.
    ```
    Once all `24` units of sand shown above have come to rest, all further
     sand flows out the bottom, falling into the endless void. Just for
    fun, the path any new sand takes before falling forever is shown here
    with `~`:
    ```
    .......+...
    .......~...
    ......~o...
    .....~ooo..
    ....~#ooo##
    ...~o#ooo#.
    ..~###ooo#.
    ..~..oooo#.
    .~o.ooooo#.
    ~#########.
    ~..........
    ~..........
    ~..........
    ```
    Using your scan, simulate the falling sand. *How many units of sand
    come to rest before sand starts flowing into the abyss below?*
    """
    graph = input_data
    r = "c"
    for i in range(10000):
        if r != "c":
            r = input("Continue? ")
            graph.draw()
        if not graph.add_sand():
            break
    answer = len(graph.sand)
    return answer


def solve_part_two(input_data):
    """Solve part two.

    You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

    You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

    In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. (This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.) With the added floor, the example above now looks like this:

            ...........+........
            ....................
            ....................
            ....................
            .........#...##.....
            .........#...#......
            .......###...#......
            .............#......
            .............#......
            .....#########......
            ....................
    <-- etc #################### etc -->

    To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, blocking the source entirely and stopping the flow of sand into the cave. In the example above, the situation finally looks like this after 93 units of sand come to rest:

    ............o............
    ...........ooo...........
    ..........ooooo..........
    .........ooooooo.........
    ........oo#ooo##o........
    .......ooo#ooo#ooo.......
    ......oo###ooo#oooo......
    .....oooo.oooo#ooooo.....
    ....oooooooooo#oooooo....
    ...ooo#########ooooooo...
    ..ooooo.......ooooooooo..
    #########################

    Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?
    """
    graph = input_data
    bottom = graph.height
    graph.height = graph.height + 4
    graph.add_bottom(bottom)
    r = "c"
    for i in track(range(10000)):
        if r != "c":
            r = input("Continue? ")
            graph.draw()
        if not graph.add_sand():
            break
    else:
        graph.draw()
        raise ValueError("Couldn't stop the sand!")
    answer = len(graph.sand)
    return answer


def main():
    puzzle = Puzzle(year=2022, day=14)
    # parsed_data = parse(puzzle.input_data)
    # answer_a = solve_part_one(parsed_data)
    # if answer_a:
    #     puzzle.answer_a = answer_a
    parsed_data = parse(puzzle.input_data)
    answer_b = solve_part_two(parsed_data)
    if answer_b:
        puzzle.answer_b = answer_b


if __name__ == "__main__":
    main()
