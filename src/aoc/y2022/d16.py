#!/usr/bin/env python
"""Solutions for AoC 16, 2022."""
# Created: 2022-12-16 19:57:08.976856

from collections import defaultdict
from itertools import product
from math import inf as INFINITY
from typing import Optional, Tuple

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import inspect, print
from rich.progress import track

from aoc.utils.pathfinding import (
    Location,
    PriorityQueue,
    Queue,
    WeightedGraph,
    breadth_first_search,
    reconstruct_path,
)


class Valve:
    def __init__(self, name, flow_rate, neighbors):
        self.name: str = name
        self.flow_rate: int = flow_rate
        self.neighbors: list[str] = neighbors
        self.is_closed = True

    def __str__(self):
        # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
        return f"Valve {self.name} has flow rate={self.flow_rate}; tunnels lead to valves {', '.join(self.neighbors)}"


class Volcano(WeightedGraph):
    def __init__(self, nodes: dict[str, Valve]):
        super().__init__()
        self.nodes: dict[str, Valve] = nodes
        self.distances: dict[str, str] = self.calculate_distances()

    def neighbors(self, id: Location) -> list[Location]:
        ret = self.nodes[id].neighbors
        if self.nodes[id].is_closed:
            ret += [id]
        return ret

    def cost(self, from_id: Location, to_id: Location, time_left: int = 0) -> float:
        """Return the cost of going from one node to another."""
        # when at a node we can:
        # * Open the valve
        # * Go to another valve
        # * Going to another valve costs:
        #   The sum of the value of the other nodes that are not open
        #   (including this one)
        #   The value of a node = (time_left - distance) * flow_rate
        print(f"{from_id} -> {to_id}")
        total = 0
        for id, node in self.nodes.items():
            if id == to_id or node.flow_rate == 0:
                continue
            if node.is_closed:
                distance = self.distances[from_id][id]
                # value is the time left minus distance minus time to open it
                value = (time_left - distance - 1) * node.flow_rate
                print(f"{id} is worth {value}")
                total += value
        return total

    def calculate_distances(self):
        distances: dict[str] = defaultdict(dict)
        for start, goal in track(
            product(self.nodes, self.nodes),
            description="Calculating distances between nodes",
        ):
            distance = (
                len(
                    reconstruct_path(
                        breadth_first_search(self, start, goal), start, goal
                    )
                )
                - 1
            )
            distances[start][goal] = distance
        return distances

    def __str__(self):
        # Valves BB and DD are open, releasing 33 pressure.
        open_valves = sorted(
            [self.nodes[v].name for v in self.nodes if not self.nodes[v].is_closed]
        )
        if len(open_valves) > 1:
            ret = (
                f"Valves {', '.join(open_valves[:-1])}, and {open_valves[-1]} are open,"
            )
        elif len(open_valves) == 1:
            ret = f"Valve {open_valves[0]} is open,"
        else:
            ret = "No valves are open."
            return ret
        ret += f" releasing {sum(v.flow_rate for _, v in self.nodes.items() if not v.is_closed)}"
        return ret


def parse_line(line: str) -> Tuple[str, int, list]:
    """Parse valve line

    Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
      0    1  2    3      %d    5      6    7   8     9:
    Return:
    AA
    0
    (DD, II, BB)
    """
    line = line.split(" ", maxsplit=9)
    name = line[1]
    rate = int(line[4].split("=")[1].strip(";"))
    neighbors = [n.strip() for n in line[9].split(",")]
    return name, rate, neighbors


def walk_volcano(graph: WeightedGraph, minutes: int = 30):
    """Use DFS algorithm to walk volcano for steps."""
    start = "AA"
    frontier = Queue()
    frontier.put(start)
    came_from: dict[Location, Optional[Location]] = {}
    total_pressure = 0

    r = "r"
    for minute in range(minutes, 0, -1):
        current: Location = frontier.get()
        if r != "c":
            # == Minute 1 ==
            # No valves are open.
            # You move to valve DD.
            print(f"== Minute {minutes - minute} ==")
            print(graph)
            r = input("Continue? ")

        min_cost = float("inf")
        next_node = None
        node_costs = {}
        for next in graph.neighbors(current):
            if node_costs.get(next, 0) > 0:
                continue
            new_cost = graph.cost(current, next, minute)
            node_costs[next] = new_cost
            if r != "c":
                print(f"{next} costs {new_cost} vs {min_cost}")
                r = input("Continue? ")

            if new_cost > min_cost:
                continue
            else:
                min_cost, next_node = new_cost, next
        assert next_node is not None
        if next_node == current:
            graph.nodes[current].is_closed = False
            # subtract one from the minute because it takes a minute to open a valve
            total_pressure += (minute - 1) * graph.nodes[current].flow_rate
        frontier.put(next_node)
        came_from[next_node] = current

    return total_pressure


# from https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/
def calculate_distances(graph):
    """Calculate all distances between nodes."""
    # Uses the floyd warshall algorithm
    distances = defaultdict(lambda: defaultdict(lambda: INFINITY))

    # initialize some items correctly
    for name, node in graph.nodes.items():
        distances[name][name] = 0

        for neighbor in node.neighbors:
            distances[name][neighbor] = 1
            distances[neighbor][neighbor] = 0

    # for every node
    for k in graph.nodes:
        # for every node
        for i in graph.nodes:
            # for every node
            for j in graph.nodes:
                # the distance between i and j is the minimum of
                distances[i][j] = min(
                    # the distance between them directly
                    # and the distance between them and another intermediate node
                    distances[i][j],
                    distances[i][k] + distances[k][j],
                )
    return distances


def parse(input_data):
    """Transform the data"""
    # Should I convert the graph to remove loops?
    valves = {}
    for line in input_data.splitlines():
        name, flow_rate, neighbors = parse_line(line)
        valve = Valve(name, flow_rate, neighbors)
        valves[name] = valve
    # Update valve neighbors
    # for name, valve in valves.items():
    #     valve.neighbors = [valves[neighbor] for neighbor in valve.neighbors]

    volcano = Volcano(valves)
    inspect(volcano.distances)
    return volcano


def solve_part_one(input_data):
    """Solve part one.

        # --- Day 16: Proboscidea Volcanium ---
    The sensors have led you to the origin of the distress signal: yet
    another handheld device, just like the one the Elves gave you.
    However, you don't see any Elves around; instead, the device is
    surrounded by elephants! They must have gotten lost in these tunnels,
    and one of the elephants apparently figured out how to turn on the
    distress signal.
    The ground rumbles again, much stronger this time. What kind of cave
    is this, exactly? You scan the cave with your handheld device; it
    reports mostly igneous rock, some ash, pockets of pressurized gas,
    magma... this isn't just a cave, it's a volcano!
    You need to get the elephants out of here, quickly. Your device
    estimates that you have *30 minutes* before the volcano erupts, so you
     don't have time to go back out the way you came in.
    You scan the cave for other options and discover a network of pipes
    and pressure-release *valves*. You aren't sure how such a system got
    into a volcano, but you don't have time to complain; your device
    produces a report (your puzzle input) of each valve's *flow rate* if
    it were opened (in pressure per minute) and the tunnels you could use
    to move between the valves.
    There's even a valve in the room you and the elephants are currently
    standing in labeled `AA`. You estimate it will take you one minute to
    open a single valve and one minute to follow any tunnel from one valve
     to another. What is the most pressure you could release?
    For example, suppose you had the following scan output:
    ```
    Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    Valve BB has flow rate=13; tunnels lead to valves CC, AA
    Valve CC has flow rate=2; tunnels lead to valves DD, BB
    Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
    Valve EE has flow rate=3; tunnels lead to valves FF, DD
    Valve FF has flow rate=0; tunnels lead to valves EE, GG
    Valve GG has flow rate=0; tunnels lead to valves FF, HH
    Valve HH has flow rate=22; tunnel leads to valve GG
    Valve II has flow rate=0; tunnels lead to valves AA, JJ
    Valve JJ has flow rate=21; tunnel leads to valve II
    ```
    All of the valves begin *closed*. You start at valve `AA`, but it must
     be damaged or *jammed* or something: its flow rate is `0`, so there's
     no point in opening it. However, you could spend one minute moving to
     valve `BB` and another minute opening it; doing so would release
    pressure during the remaining *28 minutes* at a flow rate of `13`, a
    total eventual pressure release of `28 * 13 = 364`. Then, you could
    spend your third minute moving to valve `CC` and your fourth minute
    opening it, providing an additional *26 minutes* of eventual pressure
    release at a flow rate of `2`, or `52` total pressure released by
    valve `CC`.
    Making your way through the tunnels like this, you could probably open
     many or all of the valves by the time 30 minutes have elapsed.
    However, you need to release as much pressure as possible, so you'll
    need to be methodical. Instead, consider this approach:
    ```
    == Minute 1 ==
    No valves are open.
    You move to valve DD.
    == Minute 2 ==
    No valves are open.
    You open valve DD.
    == Minute 3 ==
    Valve DD is open, releasing 20 pressure.
    You move to valve CC.
    == Minute 4 ==
    Valve DD is open, releasing 20 pressure.
    You move to valve BB.
    == Minute 5 ==
    Valve DD is open, releasing 20 pressure.
    You open valve BB.
    == Minute 6 ==
    Valves BB and DD are open, releasing 33 pressure.
    You move to valve AA.
    == Minute 7 ==
    Valves BB and DD are open, releasing 33 pressure.
    You move to valve II.
    == Minute 8 ==
    Valves BB and DD are open, releasing 33 pressure.
    You move to valve JJ.
    == Minute 9 ==
    Valves BB and DD are open, releasing 33 pressure.
    You open valve JJ.
    == Minute 10 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve II.
    == Minute 11 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve AA.
    == Minute 12 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve DD.
    == Minute 13 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve EE.
    == Minute 14 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve FF.
    == Minute 15 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve GG.
    == Minute 16 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve HH.
    == Minute 17 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You open valve HH.
    == Minute 18 ==
    Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
    You move to valve GG.
    == Minute 19 ==
    Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
    You move to valve FF.
    == Minute 20 ==
    Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
    You move to valve EE.
    == Minute 21 ==
    Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
    You open valve EE.
    == Minute 22 ==
    Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
    You move to valve DD.
    == Minute 23 ==
    Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
    You move to valve CC.
    == Minute 24 ==
    Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
    You open valve CC.
    == Minute 25 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
    == Minute 26 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
    == Minute 27 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
    == Minute 28 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
    == Minute 29 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
    == Minute 30 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
    ```
    This approach lets you release the most pressure possible in 30
    minutes with this valve layout, `1651`.
    Work out the steps to release the most pressure in 30 minutes. *What
    is the most pressure you can release?*
    """
    answer = walk_volcano(input_data)
    return answer


def solve_part_two(input_data):
    """Solve part two."""
    answer = None
    return answer


def main():
    puzzle = Puzzle(year=2022, day=16)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2022).get((2022, 16), {})
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
