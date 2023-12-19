#!/usr/bin/env python
"""Solutions for AoC 13, 2023."""
# Created: 2023-12-15 08:03:12.651146

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print


class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.height = len(graph)
        self.width = len(graph[0])

    def __repr__(self):
        ret = "\n".join("".join(row) for row in self.graph)
        return ret


def parse(input_data):
    """Transform the data.

    The data is a set of graphs

    """
    graphs = input_data.split("\n\n")
    parsed_graphs = []
    for graph in graphs:
        new_graph = []
        for row in graph.splitlines():
            new_row = []
            for column in row:
                new_row.append(column)
            new_graph.append(new_row)
        parsed_graphs.append(Graph(new_graph))
    return parsed_graphs


def get_vertical_middle(graph: Graph):
    """Given a graph, find the middle line where it mirrors"""
    # This wasn't working at first.
    middle_column = -1
    # subtract 1 from the width because we can't mirror the last column
    for column in range(graph.width - 1):
        # I want to check the column to the right and the current column
        # before starting to change
        # add 1 to the column so that we cover the full range
        for delta in range(column + 1):
            right_column = column + delta + 1
            left_column = column - delta
            if left_column < 0 or right_column >= graph.width:
                middle_column = max(middle_column, column)
                break
            right_column = [row[right_column] for row in graph.graph]
            left_column = [row[left_column] for row in graph.graph]
            if left_column != right_column:
                break
        else:
            middle_column = column
    return middle_column


def get_horizontal_middle(graph: Graph):
    """Given a graph, find the middle line where it mirrors"""
    middle_index = -1
    for row in range(graph.height - 1):
        for delta in range(row + 1):
            bottom_row = row + delta + 1
            top_row = row - delta
            if top_row < 0 or bottom_row >= graph.height:
                middle_index = max(middle_index, row)
                break
            bottom_row = graph.graph[bottom_row]
            top_row = graph.graph[top_row]
            if bottom_row != top_row:
                break
        else:
            middle_index = row
    return middle_index


def solve_part_one(input_data):
    """Solve part one.

    To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection;
    to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above
    example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4
    rows above it, a total of 405.
    """
    answer = 0
    for graph in input_data:
        middle_column = get_vertical_middle(graph)
        if middle_column != -1:
            print(f"Middle column: {middle_column}")
            answer += middle_column + 1
            continue
        middle_row = get_horizontal_middle(graph)
        if middle_row != -1:
            print(f"Middle row: {middle_row}")
            answer += (middle_row + 1) * 100
            continue
        if middle_column == -1 and middle_row == -1:
            print("########################################")
            print(graph)
    return answer


def solve_part_two(input_data):
    """Solve part two."""
    answer = None
    return answer


def main():
    puzzle = Puzzle(year=2023, day=13)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 13), {})
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
