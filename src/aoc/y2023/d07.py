#!/usr/bin/env python
"""Solutions for AoC 7, 2023."""
# Created: 2023-12-07 09:32:38.755179

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from collections import Counter, defaultdict
from functools import cmp_to_key, cache


def parse(input_data):
    """Transform the data"""
    parsed_data = {}
    for line in input_data.splitlines():
        hand, bid = line.split()
        parsed_data[hand] = int(bid)
    return parsed_data


CARD_VALUES = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARD_INDEX = {card: index for index, card in enumerate(CARD_VALUES)}

CARD_VALUES_2 = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
CARD_INDEX_2 = {card: index for index, card in enumerate(CARD_VALUES_2)}


def get_optimum_hand(hand):
    """Given a hand, get the optimum hand"""
    sorted_hand = sorted(hand, key=lambda x: CARD_INDEX_2[x])
    wild_hand = Counter(sorted_hand)
    if hand == "JJJJJ":
        return "AAAAA"
    try:
        most_common_card = Counter(
            sorted(hand.replace("J", ""), key=lambda x: CARD_INDEX_2[x])
        ).most_common()[0][0]
    except IndexError:
        print(f"hand: {hand} replaced: {hand.replace('J', '')}")
        raise
    wild_hand[most_common_card] += wild_hand["J"]
    wild_hand["J"] = 0
    return hand.replace("J", most_common_card)


# sorted calculates a key value which doesn't work in this way
# need to first group the hands and then sort


def get_hand_type(hand):
    """Given a hand of cards, calculate its type:

    0: high card value
    1: one pair
    2: two pair
    3: 3 of a kind
    4: full house
    5: 4 of a kind
    6: 5 of a kind
    """
    # sort by the highest card value first
    # this way the Counter always has the highest card value first
    hand_counts = Counter(hand).most_common()
    if hand_counts[0][1] == 1:  # all cards are the same count
        return 0
    if len(hand_counts) == 1:  # all cards are the same type
        return 6
    if hand_counts[0][1] == 4:  # four of a kind
        return 5
    if hand_counts[0][1] == 3:  # three of a kind or full house
        if hand_counts[1][1] == 2:  # full house
            return 4
        return 3
    if hand_counts[0][1] == 2:  # one pair or two pair
        if hand_counts[1][1] == 2:  # two pair
            return 2
        return 1
    raise ValueError("Unknown hand type", hand_counts)


def sort_hands_part_1(left_hand, right_hand):
    """Sort two hands of cards.

    Given a character set of  A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2

    And a hand type of:

    * Five of a kind, where all five cards have the same label: AAAAA
    * Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    * Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    * Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    * Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    * One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    * High card, where all cards' labels are distinct: 23456

    If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each
    hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card
    in each hand have the same label, however, then move on to considering the second card in each hand. If they differ,
    the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth,
    then the fifth.

    If it returns a positive number: x > y
    If it returns 0: x == y
    If it returns a negative number: x < y
    """
    left = Counter(left_hand)
    right = Counter(right_hand)
    # compare hand type
    for index in range(len(left)):
        left_most_common_count = left.most_common()[index][1]
        right_most_common_count = right.most_common()[index][1]
        if left_most_common_count > right_most_common_count:
            return 1
        if right_most_common_count < left_most_common_count:
            return -1
    else:
        # both hands have the same type
        for left_card, right_card in zip(left_hand, right_hand):
            if CARD_INDEX[left_card] == CARD_INDEX[right_card]:
                continue
            return CARD_INDEX[right_card] - CARD_INDEX[left_card]
    return 0


def solve_part_one(input_data):
    """Solve part one.

    Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's
    bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are
    6440.
    """
    grouped_hands = sorted(input_data.keys(), key=get_hand_type)
    sorted_hands = sorted(grouped_hands, key=cmp_to_key(sort_hands_part_1))
    answer = 0
    for rank, hand in enumerate(sorted_hands):
        answer += (rank + 1) * input_data[hand]
    return answer


@cache
def get_hand_key(hand):
    hand_key = [CARD_VALUES_2.index(card) for card in hand]
    print(f"{hand} -> {hand_key}")
    return hand_key


def sort_hands(hands):
    optimum_hands = {get_optimum_hand(hand): hand for hand in hands}

    print(f"Optimum: {optimum_hands}")
    grouped_wild_hands = sorted(optimum_hands.keys(), key=get_hand_type)
    hand_types = defaultdict(list)
    for hand in optimum_hands.keys():
        hand_type = get_hand_type(hand)
        hand_types[hand_type].append(hand)
    for hand_type, hands in hand_types.items():
        hand_types[hand_type] = sorted(hands, key=get_hand_key, reverse=True)
    print(hand_types)

    valid_hand_types = sorted(hand_types.keys())
    grouped_hands = []
    for i in valid_hand_types:
        print(hand_types[i])
        grouped_hands.extend(optimum_hands[hand] for hand in hand_types[i])
    # grouped_hands = [optimum_hands[hand] for hand in grouped_wild_hands]

    return grouped_hands


def rank_hands(input_data):
    """Rank hands with jokers wild."""
    optimum_hands = {get_optimum_hand(hand): hand for hand in input_data.keys()}

    print(f"Optimum: {optimum_hands}")
    grouped_wild_hands = sorted(optimum_hands.keys(), key=get_hand_type)
    hand_types = defaultdict(list)
    for hand in optimum_hands.keys():
        hand_type = get_hand_type(hand)
        hand_types[hand_type].append(hand)
    for hand_type, hands in hand_types.items():
        hand_types[hand_type] = sorted(hands, key=get_hand_key, reverse=True)
    print(hand_types)

    valid_hand_types = sorted(hand_types.keys())
    grouped_hands = []
    for i in valid_hand_types:
        print(hand_types[i])
        grouped_hands.extend(optimum_hands[hand] for hand in hand_types[i])
    # grouped_hands = [optimum_hands[hand] for hand in grouped_wild_hands]

    print(f"Grouped: {grouped_hands}")
    return grouped_hands


def solve_part_two(input_data):
    """Solve part two.

    To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers -
    wildcards that can act like whatever card would make the hand the strongest type possible.

    To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same
    order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

    J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now
    considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always
    treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.
    """
    answer = 0
    print(f"Unsorted: {input_data.keys()}")
    sorted_hands = rank_hands(input_data)
    print(f"Sorted: {sorted_hands}")
    answer = 0
    for rank, hand in enumerate(sorted_hands):
        answer += (rank + 1) * input_data[hand]
    return answer


def main():
    puzzle = Puzzle(year=2023, day=7)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 7), {})
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
