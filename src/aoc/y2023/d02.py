#!/usr/bin/env python
"""Solutions for AoC 2, 2023."""
# Created: 2023-12-02 08:29:51.109945

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from collections import defaultdict


def parse_game(game):
    id = game.split(":")[0].split(" ")[1]
    parsed_game = []
    rounds = game.split(":")[1]
    for round in rounds.split(";"):
        parsed_round = defaultdict(int)
        sets = round.split(",")
        for game_set in sets:
            amount, color = game_set.strip().split(" ")
            parsed_round[color] = int(amount)
        assert len(parsed_round) > 0
        parsed_game.append(parsed_round)
    return int(id), parsed_game


def parse(input_data):
    """Transform the data.

    The input of:

    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

    Should become:

    [
        [ { "blue": 3, "red": 4}, {"red": 1, "green": 2, "blue": 6}, { "green": 2} ]
    ]

    etc

    """
    parsed_data = []
    for game in input_data.splitlines():
        id, parsed_game = parse_game(game)
        parsed_data.append(parsed_game)
        assert id == len(parsed_data)
    return parsed_data


def solve_part_one(input_data):
    """Solve part one.

    The Elf would first like to know which games would have been possible if the bag contained only:

    12 red cubes
    13 green cubes
    and 14 blue cubes?
    """
    max_red, max_green, max_blue = 12, 13, 14
    valid_games = []
    for game_id, game in enumerate(input_data):
        valid_game = True
        for game_set in game:
            if game_set["red"] > max_red:
                valid_game = False
                break
            if game_set["blue"] > max_blue:
                valid_game = False
                break
            if game_set["green"] > max_green:
                valid_game = False
                break
        if valid_game:
            valid_games.append(game_id + 1)

    answer = sum(valid_games)
    return answer


def score_game(game):
    """Find the minimum number of marbles needed for a game and then score it.

    The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
    The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36,
    respectively. Adding up these five powers produces the sum 2286."""

    max_red, max_blue, max_green = 0, 0, 0
    for game_set in game:
        max_red = max(max_red, game_set["red"])
        max_blue = max(max_blue, game_set["blue"])
        max_green = max(max_green, game_set["green"])
    return max_red * max_blue * max_green


def solve_part_two(input_data):
    """Solve part two.

    As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of
    cubes of each color that could have been in the bag to make the game possible?
    """
    answer = 0
    for game in input_data:
        game_score = score_game(game)
        answer += game_score
    return answer


def main():
    puzzle = Puzzle(year=2023, day=2)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 2), {})
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
