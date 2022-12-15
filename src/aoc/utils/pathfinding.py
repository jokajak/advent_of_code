#!/usr/bin/env python
# From https://www.redblobgames.com/pathfinding/a-star/implementation.html

import collections
import heapq
from typing import Iterator, Optional, Protocol, T, Tuple, TypeVar

Location = TypeVar("Location")


class Graph(Protocol):
    def neighbors(self, id: Location) -> list[Location]:
        pass


class SimpleGraph(object):
    """Simple graph object"""

    def __init__(self):
        self.edges: dict[Location, list[Location]] = {}

    def neighbors(self, id: Location) -> list[Location]:
        """Return the list of neighbors for a location in the simple graph"""
        return self.edges[id]


class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self) -> bool:
        return not self.elements

    def put(self, x: T):
        self.elements.append(x)

    def get(self) -> T:
        return self.elements.popleft()


GridLocation = Tuple[int, int]


class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: list[GridLocation] = []

    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0:
            neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results


class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float:
        pass


class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: dict[GridLocation, int] = {}

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> int:
        return self.weights.get(to_node, 1)

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0:
            neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results


def dijkstra_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


def reconstruct_path(
    came_from: dict[Location, Location],
    start: Location,
    goal: Location,
    reverse: bool = True,
    add_start: bool = True,
) -> list[Location]:

    current: Location = goal
    path: list[Location] = []
    if goal not in came_from:  # no path was found
        return []
    while current != start:
        path.append(current)
        current = came_from[current]
    if add_start:
        path.append(start)  # optional
    if reverse:
        path.reverse()  # optional
    return path


def draw_grid(graph, y_min=0, x_min=0, **style):
    if "trim" in style and style["trim"]:
        print("_" * graph.width)
    else:
        print("___" * graph.width)
    for y in range(y_min, graph.height):
        for x in range(x_min, graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    if "trim" in style and style["trim"]:
        print("~" * graph.width)
    else:
        print("~~~" * graph.width)


# utility functions for dealing with square grids
def from_id_width(id, width):
    return (id % width, id // width)


def draw_tile(graph, id, style):
    r = " . "
    if "number" in style and id in style["number"]:
        r = " %-2d" % style["number"][id]
    if "letter" in style and id in style["letter"]:
        r = " %s " % style["letter"][id]
    if "point_to" in style and style["point_to"].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style["point_to"][id]
        if x2 == x1 + 1:
            r = " > "
        if x2 == x1 - 1:
            r = " < "
        if y2 == y1 + 1:
            r = " v "
        if y2 == y1 - 1:
            r = " ^ "
    if "path" in style and id in style["path"]:
        r = " @ "
    if "start" in style and id == style["start"]:
        r = " A "
    if "goal" in style and id == style["goal"]:
        r = " Z "
    if id in graph.walls:
        if style.get("trim", False):
            r = "#"
        else:
            r = "###"
    if "sand" in style and id in style["sand"]:
        if style.get("trim", False):
            r = "o"
        else:
            r = "ooo"
    if style.get("trim", False):
        r = r.strip()
    return r


def heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            print("Made it")
            break

        neighbors = graph.neighbors(current)
        # print(f"{current} neighbors: {neighbors} {goal}")
        for next in neighbors:
            # print(f"{current} {next} {graph.nodes[current]}")
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far
