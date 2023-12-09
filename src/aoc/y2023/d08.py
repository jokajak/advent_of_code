#!/usr/bin/env python
"""Solutions for AoC 8, 2023."""
# Created: 2023-12-08 08:41:12.821648

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from math import gcd


def parse(input_data):
    """Transform the data"""
    input_data = input_data.splitlines()

    directions = input_data.pop(0)  # get the first line
    input_data.pop(0)  # strip the blank line

    nodes = {}
    for line in input_data:
        node, turns = line.split(" = ")
        turns = turns.replace("(", "").replace(")", "").split(", ")
        nodes[node] = turns

    return directions, nodes


def generate_turns(directions):
    index = 0
    total_directions = len(directions)
    turns = {"L": 0, "R": 1}
    total_steps = 10**5  # 10 raised to the power 5
    # total_steps = 10  # for testing
    for index in range(total_steps):
        yield turns[directions[index % total_directions]]
    raise ValueError


def solve_part_one(input_data):
    """Solve part one.

    It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel
    follow the same instructions, you can escape the haunted wasteland!

    After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and
    you have to follow the left/right instructions until you reach ZZZ.

    This format defines each node of the network individually. For example:

    RL

    AAA = (BBB, CCC)
    BBB = (DDD, EEE)
    CCC = (ZZZ, GGG)
    DDD = (DDD, DDD)
    EEE = (EEE, EEE)
    GGG = (GGG, GGG)
    ZZZ = (ZZZ, ZZZ)

    Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In
    this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the
    left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.
    """
    steps = 0
    directions, nodes = input_data
    current_node = "AAA"
    for turn in generate_turns(directions):
        steps += 1
        current_node = nodes[current_node][turn]
        if current_node == "ZZZ":
            break
    answer = steps
    return answer


def solve_part_two(input_data):
    """Solve part two.

    The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had the camel follow the
    instructions, but you've barely left your starting position. It's going to take significantly more steps to
    escape!

    What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of spacetime?
    Only one way to find out.

    After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names
    ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at every node that
    ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with
    Z.

    For example:

    LR

    11A = (11B, XXX)
    11B = (XXX, 11Z)
    11Z = (11B, XXX)
    22A = (22B, XXX)
    22B = (22C, 22C)
    22C = (22Z, 22Z)
    22Z = (22B, 22B)
    XXX = (XXX, XXX)

    Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each left/right
    instruction, use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat this
    process until all of the nodes you're currently on end with Z. (If only some of the nodes you're on end with Z, they
    act like any other node and you continue as normal.) In this example, you would proceed as follows:

        Step 0: You are at 11A and 22A.
        Step 1: You choose all of the left paths, leading you to 11B and 22B.
        Step 2: You choose all of the right paths, leading you to 11Z and 22C.
        Step 3: You choose all of the left paths, leading you to 11B and 22Z.
        Step 4: You choose all of the right paths, leading you to 11Z and 22B.
        Step 5: You choose all of the left paths, leading you to 11B and 22C.
        Step 6: You choose all of the right paths, leading you to 11Z and 22Z.

    So, in this example, you end up entirely on nodes that end in Z after 6 steps.

    Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that
    end with Z?
    """
    # I need to find the number of steps from each start node to each end node
    # Then I need to find the least common multiple for the set of start node to end node
    directions, nodes = input_data
    start_nodes = set(node for node in nodes.keys() if node.endswith("A"))
    end_nodes = set(node for node in nodes if node.endswith("Z"))
    node_paths = {}
    # print(f"Starts: {start_nodes}")
    # print(f"Ends: {end_nodes}")
    for start_node in start_nodes:
        print(f"Finding paths for {start_node}")
        steps = 0
        end_nodes_reached = {}
        turns_taken = []
        current_node = start_node
        for turn in generate_turns(directions):
            steps += 1
            # print( f"At {current_node}: {nodes[current_node]} -> {nodes[current_node][turn]}")
            next_node = nodes[current_node][turn]
            if next_node.endswith("Z"):
                print(f"Reached an end: {next_node}")
                if next_node not in end_nodes_reached:
                    end_nodes_reached[next_node] = steps
                    break
                # print(f"{start_node}: {end_nodes_reached}")
            turn_to_take = (current_node, turn, next_node)
            # print(f"Turns taken: {turns_taken}")
            current_node = next_node
            # if turn_to_take in turns_taken:  # we've already taken this turn, break
            #     print(f"Stopping after finding a turn we already took")
            #     break
            turns_taken.append(turn_to_take)
            if (
                set(end_nodes_reached.keys()) == end_nodes
            ):  # we've reached all end nodes
                break
        node_paths[start_node] = end_nodes_reached

    # We have all the minimum path lengths, calculate the least common multiple for all starts

    def lcm_of_list(numbers):
        def lcm(x, y):
            return x * y // gcd(x, y)

        result = 1
        for number in numbers:
            result = lcm(result, number)

        return result

    print(node_paths)
    # assume only one end per start
    all_path_lengths = []
    for path_lengths in node_paths.values():
        for path_length in path_lengths.values():
            all_path_lengths.append(path_length)
    answer = lcm_of_list(all_path_lengths)
    print(answer)
    return answer


def main():
    puzzle = Puzzle(year=2023, day=8)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 8), {})
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
