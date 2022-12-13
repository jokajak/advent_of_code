#!/usr/bin/env python
"""Test pathfinding library"""

from typing import Optional

from aoc.utils.pathfinding import (
    Graph,
    GridWithWeights,
    Location,
    Queue,
    SimpleGraph,
    SquareGrid,
    dijkstra_search,
    draw_grid,
    from_id_width,
    reconstruct_path,
)

# data from main article
DIAGRAM1_WALLS = [
    from_id_width(id, width=30)
    for id in [
        21,
        22,
        51,
        52,
        81,
        82,
        93,
        94,
        111,
        112,
        123,
        124,
        133,
        134,
        141,
        142,
        153,
        154,
        163,
        164,
        171,
        172,
        173,
        174,
        175,
        183,
        184,
        193,
        194,
        201,
        202,
        203,
        204,
        205,
        213,
        214,
        223,
        224,
        243,
        244,
        253,
        254,
        273,
        274,
        283,
        284,
        303,
        304,
        313,
        314,
        333,
        334,
        343,
        344,
        373,
        374,
        403,
        404,
        433,
        434,
    ]
]


def breadth_first_search(graph: Graph, start: Location):
    # print out what we find
    frontier = Queue()
    frontier.put(start)
    came_from: dict[Location, Optional[Location]] = {}
    came_from[start] = None

    while not frontier.empty():
        current: Location = frontier.get()
        if current:
            print(f"  Visiting {current}")
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    return came_from


if __name__ == "__main__":
    example_graph = SimpleGraph()
    example_graph.edges = {
        "A": ["B"],
        "B": ["C"],
        "C": ["B", "D", "F"],
        "D": ["C", "E"],
        "E": ["F"],
        "F": [],
    }

    print("Reachable from A:")
    breadth_first_search(example_graph, "A")
    print("Reachable from E:")
    breadth_first_search(example_graph, "E")

    g = SquareGrid(30, 15)
    g.walls = DIAGRAM1_WALLS  # long list, [(21, 0), (21, 2), ...]
    draw_grid(g)

    start = (8, 7)
    parents = breadth_first_search(g, start)
    draw_grid(g, point_to=parents, start=start)

    diagram4 = GridWithWeights(10, 10)
    diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
    diagram4.weights = {
        loc: 5
        for loc in [
            (3, 4),
            (3, 5),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
            (4, 5),
            (4, 6),
            (4, 7),
            (4, 8),
            (5, 1),
            (5, 2),
            (5, 3),
            (5, 4),
            (5, 5),
            (5, 6),
            (5, 7),
            (5, 8),
            (6, 2),
            (6, 3),
            (6, 4),
            (6, 5),
            (6, 6),
            (6, 7),
            (7, 3),
            (7, 4),
            (7, 5),
        ]
    }

    start, goal = (1, 4), (8, 3)
    came_from, cost_so_far = dijkstra_search(diagram4, start, goal)
    draw_grid(diagram4, point_to=came_from, start=start, goal=goal)
    print()
    draw_grid(diagram4, path=reconstruct_path(came_from, start=start, goal=goal))
