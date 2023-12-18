#!/usr/bin/env python
"""Solutions for AoC 14, 2023."""
# Created: 2023-12-15 08:03:09.032874

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from collections import defaultdict


class Graph:
    def __init__(self, graph, rock_spots):
        self.graph = graph
        self.height = len(graph)
        self.width = len(graph[0])
        self.rock_spots = rock_spots

    def __iter__(self):
        return iter([self.graph, self.rock_spots])


def parse(input_data):
    """Transform the data.

    O....#....
    O.OO#....#
    .....##...
    OO.#O....O
    .O.....O#.
    O.#..O.#.#
    ..O..#O..O
    .......O..
    #....###..
    #OO..#....
    """
    print(input_data)
    reversed_graph = defaultdict(dict)
    rock_spots = {}
    for row_index, line in enumerate(input_data.split()):
        row = reversed_graph[row_index]
        for col_index, char in enumerate(line):
            row[col_index] = char
            if char == "#":
                rock_spots[(row_index, col_index)] = True
    # convert the defaultdict to a dict so it doesn't mutate
    reversed_graph = dict(reversed_graph)
    return Graph(reversed_graph, rock_spots)


def get_load(graph):
    """Calculate the load.

    The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south
    edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the
    amount of load caused by each rock in each row is as follows:

    OOOO.#.O.. 10
    OO..#....#  9
    OO..O##..O  8
    O..#.OO...  7
    ........#.  6
    ..#....#.#  5
    ..O..#.O.O  4
    ..O.......  3
    #....###..  2
    #....#....  1

    The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.
    """

    ret = 0

    total_rows = max(graph.keys())
    for row_index, row in graph.items():
        for column_index, char in row.items():
            if char == "O":
                ret += (total_rows - row_index) + 1
    return ret


def tilt_graph(graph, delta_x=0, delta_y=-1):
    """Tilt a graph

    delta_x determines how the columns mutate
    delta_y determines how the rows mutate

    assume that the graph is defined by rows (y value) and columns (x value)
    """

    assert isinstance(graph, Graph)
    current_graph = graph
    rock_spots = graph.rock_spots
    stop_spots = dict(rock_spots)
    ret = defaultdict(dict)
    max_columns = graph.width
    max_rows = graph.height
    graph = graph.graph
    row_range_steps = (0, max_rows, 1)
    col_range_steps = (0, max_columns, 1)
    if delta_y > 0:
        row_range_steps = (max_rows, -1, -1)
    if delta_x > 0:
        col_range_steps = (max_columns, -1, -1)
    for row_index in range(*row_range_steps):
        row = graph.get(row_index, {})
        for column_index in range(*col_range_steps):
            char = row.get(column_index, ".")
            current_x, current_y = column_index, row_index
            if char == "O":
                while (
                    (current_y, current_x) not in stop_spots
                    and current_y >= 0
                    and current_x >= 0
                    and current_y < max_rows
                    and current_x < max_columns
                ):
                    new_x = current_x + delta_x
                    new_y = current_y + delta_y
                    if (
                        (new_y, new_x) in stop_spots
                        or new_y < 0
                        or new_x < 0
                        or new_y >= max_rows
                        or new_x >= max_columns
                    ):
                        break
                    # only change if we know we can
                    current_x, current_y = new_x, new_y
                stop_spots[(current_y, current_x)] = True
            ret[current_y][current_x] = char
            if current_y != row_index or current_x != column_index:
                ret[row_index][column_index] = "."
    ret = dict(ret)
    current_graph.graph = ret
    return current_graph


def print_graph(graph):
    """Print a graph"""
    out = []
    print("########################################")
    if isinstance(graph, Graph):
        width = graph.width
        height = graph.height
        graph = graph.graph
    else:
        width = len(graph[0])
        height = len(graph)
    for row_index in range(height):
        row = graph.get(row_index, {})
        out_line = []
        last_col = width
        for col in range(last_col + 1):
            out_line.append(row.get(col, "."))
        out_line = "".join(out_line)
        out_line = f"{out_line} :{row_index}"
        out.append(out_line)
    for row in out:
        print(f"{''.join(row)}")


def hash_graph(graph):
    """Hash a graph"""
    out = []
    for row_index, row in graph.items():
        out_line = []
        last_col = max(row.keys())
        for col in range(last_col + 1):
            out_line.append(row.get(col, "."))
        out_line = "".join(out_line)
        out.append(out_line)

    return "".join(out)


def solve_part_one(input_data):
    """Solve part one.

    Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support
    beams?
    """
    graph = input_data
    print_graph(graph)
    graph = tilt_graph(graph)
    print_graph(graph)
    answer = get_load(graph.graph)
    return answer


def run_cycle(graph):
    """Run a tilt cycle.

    A cycle is:
    (delta_x, delta_y):
    [0, -1],
    [-1, 0],
    [0, 1],
    [1, 0]
    """
    graph = tilt_graph(graph, delta_x=0, delta_y=-1)
    graph = tilt_graph(graph, delta_x=-1, delta_y=0)
    graph = tilt_graph(graph, delta_x=0, delta_y=1)
    graph = tilt_graph(graph, delta_x=1, delta_y=0)
    return graph


def find_repeating_interval(data):
    seen_counts = {}
    repeating_interval = None

    for i, (value, count) in enumerate(data):
        if value not in seen_counts:
            seen_counts[value] = (count, i)
        else:
            prev_count, prev_index = seen_counts[value]
            if count == prev_count and repeating_interval is None:
                repeating_interval = i - prev_index
                break

    return repeating_interval


def solve_part_two(input_data, cycles=1000000000):
    """Solve part two.

    This time we have to tilt the platform 1000000000 cycles

    A cycle is:
    (delta_x, delta_y):
    [0, -1],
    [-1, 0],
    [0, 1],
    [1, 0]
    """
    from rich.progress import track

    graph = input_data
    seen_graphs = {}
    graph_loads = {}
    cycle_length = 0

    for iteration in track(range(cycles)):
        graph = run_cycle(graph)
        # This repeats every 10, I don't know why
        graph_hash = hash_graph(graph.graph)
        if graph_hash not in seen_graphs:
            seen_graphs[graph_hash] = [iteration]
            graph_loads[graph_hash] = get_load(graph.graph)
            graph_loads[iteration] = get_load(graph.graph)
        else:
            seen_graphs[graph_hash].append(iteration)
            if len(seen_graphs[graph_hash]) == 3:
                cycle_length = iteration - seen_graphs[graph_hash][1]
                break
    min_repeating = cycles
    for hash_value, repeating_iterations in seen_graphs.items():
        if len(repeating_iterations) >= 2:
            min_repeating = min(min_repeating, min(repeating_iterations))
            print(f"{repeating_iterations}: {graph_loads[hash_value]}")

    graph_value = (cycles - min_repeating) % cycle_length + min_repeating
    print(
        f"({cycles} - {min_repeating}) % {cycle_length} + {min_repeating} = {graph_value}"
    )
    print(f"graph load: {graph_loads[graph_value]}")
    print_graph(graph)

    answer = graph_loads[graph_value]
    return answer


def main():
    puzzle = Puzzle(year=2023, day=14)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 14), {})
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
