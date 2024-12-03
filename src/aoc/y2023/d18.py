#!/usr/bin/env python
"""Solutions for AoC 18, 2023."""
# Created: 2023-12-21 22:54:39.484694

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print


def parse(input_data):
    """Transform the data

    R 6 (#70c710)
    D 5 (#0dc571)
    L 2 (#5713f0)
    D 2 (#d2c081)
    R 2 (#59c680)
    D 2 (#411b91)
    L 5 (#8ceee2)
    U 2 (#caa173)
    L 1 (#1b58a2)
    U 2 (#caa171)
    R 2 (#7807d2)
    U 3 (#a77fa3)
    L 2 (#015232)
    U 2 (#7a21e3)
    """
    parsed_data = []
    for line in input_data.splitlines():
        direction, count, rgb = line.split()
        parsed_data.append((direction, int(count), rgb))
    return parsed_data


def dig_trench(plan):
    """Dig an outline.

    Each step in the plan includes a direction, a count, and a color
    """
    node = (0, 0)
    coords = [(node, "")]
    for direction, count, rgb in plan:
        x, y = node
        delta_x = delta_y = 0
        if direction == "R":
            delta_x, delta_y = count, 0
        elif direction == "D":
            delta_x, delta_y = 0, count
        elif direction == "L":
            delta_x, delta_y = -count, 0
        elif direction == "U":
            delta_x, delta_y = 0, -count
        else:
            assert ValueError
        node = (x + delta_x, y + delta_y)
        coords.append((node, rgb))
    return coords


def get_area(coordinates):
    shoelace_area = polygonArea(coordinates)
    perimeter = get_perimeter(coordinates)
    area = shoelace_area + perimeter / 2 + 1
    return area


def get_perimeter(coordinates):
    perimeter = 0
    current_node = coordinates[0]
    for coordinate in coordinates:
        x, y = current_node
        new_x, new_y = coordinate
        delta_x = abs(x - new_x)
        delta_y = abs(y - new_y)
        perimeter += delta_x + delta_y
        current_node = coordinate
    return perimeter


def polygonArea(vertices):
    # A function to apply the Shoelace algorithm
    numberOfVertices = len(vertices)
    sum1 = 0
    sum2 = 0

    for i in range(0, numberOfVertices - 1):
        sum1 = sum1 + vertices[i][0] * vertices[i + 1][1]
        sum2 = sum2 + vertices[i][1] * vertices[i + 1][0]

    # Add xn.y1
    sum1 = sum1 + vertices[numberOfVertices - 1][0] * vertices[0][1]
    # Add x1.yn
    sum2 = sum2 + vertices[0][0] * vertices[numberOfVertices - 1][1]

    area = abs(sum1 - sum2) / 2
    return area


def solve_part_one(input_data):
    """Solve part one.

    Get the area of a polygon defined by movements."""
    answer = 0
    trench = dig_trench(input_data)
    coordinates = [coord for coord, _ in trench]
    answer = get_area(coordinates)
    return answer


def solve_part_two(input_data):
    """Solve part two.

    Get the area of a polygon defined by big movements.

    the instructions are not direction, range, rgb but instead:
    ignore, ignore, range in hexadecimal, encoded direction
    """
    answer = 0
    print(input_data)
    new_path = []
    for _, _, encoded in input_data:
        count = int(encoded[2:6], 16)  # ignore the # and convert to int
        direction = encoded[7]
        if direction == "0":
            direction = "R"
        elif direction == "1":
            direction = "D"
        elif direction == "2":
            direction = "L"
        elif direction == "3":
            direction = "U"
        else:
            raise ValueError
        new_path.append((direction, count, ""))
    trench = dig_trench(new_path)
    coordinates = [coord for coord, _ in trench]
    answer = get_area(coordinates)
    return answer


def main():
    puzzle = Puzzle(year=2023, day=18)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 18), {})
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
