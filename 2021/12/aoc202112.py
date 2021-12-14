"""AoC 12, 2021"""

# Standard library imports
import pathlib
import sys
from dataclasses import dataclass
from aocd import data as input_data, submit
from collections import defaultdict


@dataclass
class Cave(object):
    neighbors: set
    id: str
    big: bool
    is_start: bool = False
    is_end: bool = False

    def __init__(self, id) -> None:
        self.neighbors = set()
        self.id = id
        self.big = id == id.upper()
        self.is_start = id == "start"
        self.is_end = id == "end"

    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id

    def __hash__(self) -> int:
        return hash(self.id) ^ len(self.neighbors)

    def add_neighbor(self, neighbor) -> None:
        self.neighbors.add(neighbor)

    @property
    def visit_only_once(self) -> bool:
        return not self.big

    def __repr__(self) -> str:
        return self.id


def parse(puzzle_input):
    """Parse input"""
    caves = {}
    for line in puzzle_input.splitlines():
        cave_a, cave_b = line.split("-")
        cave_a = caves.setdefault(cave_a, Cave(cave_a))
        cave_b = caves.setdefault(cave_b, Cave(cave_b))
        cave_a.add_neighbor(cave_b)
        cave_b.add_neighbor(cave_a)
    return caves


def dfs(src: Cave, dst: Cave, path: list, seen: set) -> list:
    """Recursive generator that yields all paths from `src` to `dst`.

    From https://codereview.stackexchange.com/q/260737
    """
    if src in seen:
        # already tried this cave
        return

    # add the current node to the path
    new_path = (*path, src)  # same as path + [src]
    if src == dst:
        yield new_path
        return

    # some nodes cannot be re-visited
    if src.visit_only_once:
        seen.add(src)

    for neighbor in src.neighbors:
        yield from dfs(neighbor, dst, new_path, seen)

    if src.visit_only_once:
        seen.remove(src)


def part1(data):
    """Solve part 1.

    With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting out of this cave
    anytime soon is by finding a path yourself. Not just a path - the only way to know if you've found the best path is
    to find all of them.

    Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more
    than once. There are two types of caves: big caves (written in uppercase, like A) and small caves (written in
    lowercase, like b). It would be a waste of time to visit any small cave more than once, but big caves are large
    enough that it might be worth visiting them multiple times. So, all paths you find should visit small caves at most
    once, and can visit big caves any number of times.

    How many paths through this cave system are there that visit small caves at most once?
    """
    caves = data
    src = caves["start"]
    dst = caves["end"]
    paths = list(dfs(src, dst, [], set()))
    return len(paths)


def part2(data):
    """Solve part 2.

    After reviewing the available paths, you realize you might have time to visit a single small cave twice.
    Specifically, big caves can be visited any number of times, a single small cave can be visited at most twice, and
    tyhe remaining small caves can be visited at most once. However, the caves named start and end can only be visited
    exactly once each: once you leave the start cave, you may not return to it, and once you reach the end cave, the
    path must end immediately.
    """
    def dfs(src: Cave, dst: Cave, path: list, seen: dict) -> list:
        """Recursive generator that yields all paths from `src` to `dst`.

        From https://codereview.stackexchange.com/q/260737
        """
        # cannot re-enter src
        if src.is_start and len(path) > 0:
            return
        # already tried this cave
        if seen[src] > 0:
            # and another cave twice
            if max([v for _, v in seen.items()]) == 2:
                # therefore we can't enter this cave
                return

        # add the current node to the path
        new_path = (*path, src)  # same as path + [src]
        if src == dst:
            yield new_path
            return

        # some nodes cannot be re-visited
        if src.visit_only_once:
            # therefore increase the seen value by one
            seen[src] += 1

        for neighbor in src.neighbors:
            yield from dfs(neighbor, dst, new_path, seen)

        # some nodes cannot be revisited
        if src.visit_only_once:
            # now that we've processed all of its neighbors, step back in the graph
            seen[src] -= 1

    caves = data
    src = caves["start"]
    dst = caves["end"]
    paths = list(dfs(src, dst, [], defaultdict(int)))
    # print("\n".join([str(path) for path in paths]))
    return len(paths)


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
