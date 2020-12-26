#!/usr/bin/env python

import copy

import pytest
import tqdm

MAX_ROUNDS = 100000


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            ([1], [2]),
            ([], [1, 2]),
        )
    ]
)
def test_play_round(input, expected):
    assert play_round(*input) == expected


def play_round(hand_one, hand_two):
    card_one = hand_one.pop()
    card_two = hand_two.pop()
    if card_one > card_two:
        hand_one.insert(0, card_one)
        hand_one.insert(0, card_two)
    else:
        hand_two.insert(0, card_two)
        hand_two.insert(0, card_one)
    return (hand_one, hand_two)


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            [1, 2], 5
        )
    ]
)
def test_score_hand(input, expected):
    assert score_hand(input) == expected


def score_hand(hand):
    value = 0
    for i in range(len(hand)):
        value += (i+1)*hand[i]
    return value


def play_recursive_combat_round(game_rounds, hand_one, hand_two):
    card_one = hand_one.pop()
    card_two = hand_two.pop()
    winner = None
    if len(hand_one) < card_one or len(hand_two) < card_two:
        if card_one > card_two:
            winner = "PLAYER_1"
        else:
            winner = "PLAYER_2"
    else:
        # need to play recursive combat sub-game
        # print("Playing a subgame")
#        subgame_hand_one = copy.copy(hand_one[-1:-(card_one+1):-1])
#        subgame_hand_two = copy.copy(hand_two[-1:-(card_two+1):-1])
        subgame_hand_one = copy.copy(hand_one[-(card_one):])
        subgame_hand_two = copy.copy(hand_two[-(card_two):])
        # print(subgame_hand_one, subgame_hand_two)
        winner, hand = play_recursive_combat(set(), subgame_hand_one, subgame_hand_two)
    if winner == "PLAYER_1":
        hand_one.insert(0, card_one)
        hand_one.insert(0, card_two)
    elif winner == "PLAYER_2":
        hand_two.insert(0, card_two)
        hand_two.insert(0, card_one)
    return (hand_one, hand_two)


def play_recursive_combat(game_rounds, hand_one, hand_two):
    #for _ in tqdm.tqdm(range(MAX_ROUNDS)):
    for _ in range(MAX_ROUNDS):
        hand_one_hash = ",".join([str(i) for i in hand_one])
        hand_two_hash = ",".join([str(i) for i in hand_two])
        if (hand_one_hash, hand_two_hash) in game_rounds:
            return "PLAYER_1", hand_one
        else:
            game_rounds.add((hand_one_hash, hand_two_hash))
        hand_one, hand_two = play_recursive_combat_round(game_rounds, hand_one, hand_two)
        # print("Round: {}".format(_))
        if len(hand_one) == 0 or len(hand_two) == 0:
            break
    if len(hand_one) == 0:
        # print(hand_one, hand_two)
        return "PLAYER_2", hand_two
    elif len(hand_two) == 0:
        # print(hand_one, hand_two)
        return "PLAYER_1", hand_one
    else:
        raise ValueError


def main():
    hand_one, hand_two = None, None
    with open("input.txt") as f:
        for line in f.readlines():
            line = line.strip("\n")
            if line == "":
                continue
            if line == "Player 1:":
                hand_one = []
            elif line == "Player 2:":
                hand_two = []
            elif hand_two is not None:
                hand_two.insert(0, int(line))
            elif hand_one is not None:
                hand_one.insert(0, int(line))
    part_two_hand_one = copy.copy(hand_one)
    part_two_hand_two = copy.copy(hand_two)

    for _ in range(MAX_ROUNDS):
        hand_one, hand_two = play_round(hand_one, hand_two)
        if len(hand_one) == 0 or len(hand_two) == 0:
            break
    part_one = score_hand(hand_one) + score_hand(hand_two)
    print(part_one)

    winner, hand = play_recursive_combat(set(), part_two_hand_one, part_two_hand_two)
    print(score_hand(hand), hand)


if __name__ == "__main__":
    main()
