"""AoC 5, 2021"""

# Standard library imports
from dataclasses import dataclass, field
from parse import compile
from aocd import data, submit


@dataclass
class HydrothermalVents:
    """Represent hydrothermal vents for 2021 Advent of Code day 5.

    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2

    So, the horizontal and vertical lines from the above list would produce the following diagram:

    .......1..
    ..1....1..
    ..1....1..
    .......1..
    .112111211
    ..........
    ..........
    ..........
    ..........
    222111....
    In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number
    of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from
    2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.
    """

    grid: list[list] = field(default_factory=list)

    def __init__(self, max_x: int = 0, max_y: int = 0) -> None:
        # create a grid with appropriate size
        self.grid = [[0] * (max_y + 1) for _ in range(max_x + 1)]

    def add_line_segment(
        self,
        start_coordinates: tuple,
        stop_coordinates: tuple,
        ignore_diagonals: bool = True,
    ) -> None:
        start_y, start_x = start_coordinates
        stop_y, stop_x = stop_coordinates
        if ignore_diagonals:
            if (start_x != stop_x) and (start_y != stop_y):
                return
        else:
            delta_x = stop_x - start_x
            delta_y = stop_y - start_y
            if delta_x != 0 and delta_y != 0 and abs(delta_x) != abs(delta_y):
                return
        if start_x < stop_x:
            delta_x = 1
        elif start_x > stop_x:
            delta_x = -1
        else:
            delta_x = 0
        if start_y < stop_y:
            delta_y = 1
        elif start_y > stop_y:
            delta_y = -1
        else:
            delta_y = 0
        x = start_x
        y = start_y
        # This code handles diagonals well
        if delta_x == 0:
            while True:
                self.grid[x][y] += 1
                y += delta_y
                if y == stop_y:
                    self.grid[x][y] += 1
                    break
        elif delta_y == 0:
            while True:
                self.grid[x][y] += 1
                x += delta_x
                if x == stop_x:
                    self.grid[x][y] += 1
                    break
        else:
            while True:
                self.grid[x][y] += 1
                x += delta_x
                y += delta_y
                if x == stop_x or y == stop_y:
                    self.grid[x][y] += 1
                    break

    def __repr__(self) -> str:
        representation = []
        for row in self.grid:
            row_output = ""
            for column in row:
                if column == 0:
                    row_output += "."
                else:
                    row_output += str(column)
            representation.append(row_output)
        return "\n".join(representation)

    @property
    def dangerous_points(self) -> int:
        dangerous_points = 0
        for row in self.grid:
            for column in row:
                if column >= 2:
                    dangerous_points += 1
        return dangerous_points


def parse(puzzle_input):
    """Parse input"""
    parser = compile("{start_x:d},{start_y:d} -> {stop_x:d},{stop_y:d}")
    parsed_input = []
    max_x = max_y = 0
    for entry in puzzle_input.splitlines():
        res = parser.parse(entry)
        parsed_input.append(
            ((res["start_x"], res["start_y"]), (res["stop_x"], res["stop_y"]))
        )
        max_x = max(res["start_x"], res["stop_x"], max_x)
        max_y = max(res["start_y"], res["stop_y"], max_y)
    return (parsed_input, max_y, max_x)


def part1(data):
    """Solve part 1"""
    line_segments, max_x, max_y = data
    vents = HydrothermalVents(max_x, max_y)
    for entry in line_segments:
        start_coordinates, stop_coordinates = entry
        vents.add_line_segment(start_coordinates, stop_coordinates)
    return vents.dangerous_points


def part2(data):
    """Solve part 2.

    Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also
    consider diagonal lines.

    Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal,
    vertical, or a diagonal line at exactly 45 degrees. In other words:

    An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3. An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
    Considering all lines from the above example would now produce the following diagram:

    1.1....11.
    .111...2..
    ..2.1.111.
    ...1.2.2..
    .112313211
    ...1.2....
    ..1...1...
    .1.....1..
    1.......1.
    222111....

    You still need to determine the number of points where at least two lines overlap. In the above example, this is
    still anywhere in the diagram with a 2 or larger - now a total of 12 points.

    Consider all of the lines. At how many points do at least two lines overlap?
    """
    line_segments, max_x, max_y = data
    vents = HydrothermalVents(max_x, max_y)
    for entry in line_segments:
        start_coordinates, stop_coordinates = entry
        vents.add_line_segment(
            start_coordinates, stop_coordinates, ignore_diagonals=False
        )
    return vents.dangerous_points


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    answer_a, answer_b = solve(puzzle_input=data)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
