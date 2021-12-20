"""AoC 17, 2021"""

# Standard library imports
import pathlib
import sys
from parse import compile
from aocd import data as input_data, submit


def parse(puzzle_input):
    """Parse input"""
    parser = compile("target area: x={min_x:d}..{max_x:d}, y={min_y:d}..{max_y:d}")
    res = parser.parse(puzzle_input)
    return (res["min_x"], res["max_x"]), (res["min_y"], res["max_y"])


def step_trajectory(x_velocity, y_velocity):
    x_pos = y_pos = 0
    while True:
        x_pos += x_velocity
        y_pos += y_velocity
        if x_velocity > 0:
            x_velocity -= 1
        y_velocity -= 1
        yield x_pos, y_pos


def reaches_target(target: tuple, velocities: tuple) -> bool:
    x_range, y_range = target
    delta_x, delta_y = velocities
    min_x, max_x = x_range
    min_y, max_y = y_range
    # 1+5 + 2+4 + 3 = 15 = n(n+1)/2 = 15
    max_x_distance = (delta_x * (delta_x + 1))/2
    # projectile won't reach or is too fast
    if (max_x_distance < min_x) or (max_x < delta_x):
        return False
    # x won't end up in the target
    for x_pos, y_pos in step_trajectory(delta_x, delta_y):
        if (min_x <= x_pos <= max_x) and (min_y <= y_pos <= max_y):
            return True
        if x_pos > max_x or y_pos < min_y:
            return False


def part1(data):
    """Solve part 1.


    * The probe's x position increases by its x velocity.
    * The probe's y position increases by its y velocity.
    * Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater
      than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
    * Due to gravity, the probe's y velocity decreases by 1.
    """
    x_range, y_range = data
    min_x, max_x = x_range
    min_y, max_y = y_range
    valid_velocities = []
    for x in range(max_x):
        for y in (range(max(abs(min_y), abs(max_y)))):
            if reaches_target(data, (x, y)):
                valid_velocities.append((x, y))
    max_total_y = 0
    for velocity in valid_velocities:
        height = 0
        delta_x, delta_y = velocity
        while delta_y > 0:
            height += delta_y
            delta_y -= 1
        max_total_y = max(max_total_y, height)
    return max_total_y


def part2(data):
    """Solve part 2.

    To get the best idea of what your options are for launching the probe, you need to find every initial velocity that
    causes the probe to eventually be within the target area after any step.

    In the above example, there are 112 different initial velocity values that meet these criteria:
    """
    x_range, y_range = data
    min_x, max_x = x_range
    min_y, max_y = y_range
    valid_velocities = []
    min_y_velocity = min_y
    max_y_velocity = abs(min_y)
    for x in range(max_x*2):
        for y in range(min_y_velocity-1, max_x + 1):
            if reaches_target(data, (x, y)):
                valid_velocities.append((x, y))
    return len(valid_velocities)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))

    answer_a, answer_b = solve(puzzle_input=input_data)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
