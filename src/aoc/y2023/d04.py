#!/usr/bin/env python
"""Solutions for AoC 4, 2023."""
# Created: 2023-12-04 06:44:29.370755

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
from pprint import pprint


def parse(input_data):
    """Transform the data"""
    parsed_data = []
    for line in input_data.splitlines():
        card = line.split(":")[1]
        numbers_i_have, winning_numbers = card.split("|")
        numbers_i_have = numbers_i_have.strip().split(" ")
        winning_numbers = winning_numbers.strip().split(" ")
        winning_numbers = [int(entry) for entry in winning_numbers if entry]
        numbers_i_have = [int(entry) for entry in numbers_i_have if entry]
        if len(winning_numbers) != len(set(winning_numbers)):
            print(f"{winning_numbers} != {set(winning_numbers)}")
        assert len(winning_numbers) == len(set(winning_numbers))
        assert len(numbers_i_have) == len(set(numbers_i_have))
        parsed_data.append((numbers_i_have, winning_numbers))
    return parsed_data


def solve_part_one(input_data):
    """Solve part one.

    The Elf leads you over to the pile of colorful cards. There, you discover dozens of scratchcards, all with their
    opaque covering already scratched off. Picking one up, it looks like each card has two lists of numbers separated by
    a vertical bar (|): a list of winning numbers and then a list of numbers you have. You organize the information into
    a table (your puzzle input).

    As far as the Elf has been able to figure out, you have to figure out which of the numbers you have appear in the
    list of winning numbers. The first match makes the card worth one point and each match after the first doubles the
    point value of that card.
    """
    answer = 0
    for numbers_i_have, winning_numbers in input_data:
        common_cards = set(numbers_i_have).intersection(set(winning_numbers))
        if len(common_cards) > 0:
            points = 2 ** (len(common_cards) - 1)
            # print(
            #     f"{numbers_i_have}:{winning_numbers}: {set(numbers_i_have).intersection(set(winning_numbers))} ({points} points)"
            # )
            answer += points
    return answer


def solve_part_two(input_data):
    """Solve part two.

    There's no such thing as "points". Instead, scratchcards only cause you to win more scratchcards equal to the number
    of winning numbers you have.

    Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. So, if card
    10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.

    Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied.
    So, if you win a copy of card 10 and it has 5 matching numbers, it would then win a copy of the same cards that the
    original card 10 won: cards 11, 12, 13, 14, and 15. This process repeats until none of the copies cause you to win
    any more cards. (Cards will never make you copy a card past the end of the table.)

    Once all of the originals and copies have been processed, you end up with 1 instance of card 1, 2 instances of card
    2, 4 instances of card 3, 8 instances of card 4, 14 instances of card 5, and 1 instance of card 6. In total, this
    example pile of scratchcards causes you to ultimately have 30 scratchcards!
    """

    # this variable captures how many copies of a card there are
    card_counts = {}
    for current_index, entry in enumerate(input_data):
        numbers_i_have, winning_numbers = entry
        common_cards = set(numbers_i_have).intersection(set(winning_numbers))
        # if this was a scoring card, then
        if len(common_cards) > 0:
            start_index = current_index + 1
            end_index = start_index + len(common_cards)
            # for each of the cards that get copied
            for idx in range(current_index + 1, end_index):
                # set the number of copies to be the number of copies + the count of this card
                current_card_copies = card_counts.get(current_index, 0)
                next_card_copies = card_counts.get(idx, 0)
                card_counts[idx] = next_card_copies + current_card_copies + 1
            pprint(card_counts)
    answer = sum(card_counts.values()) + len(input_data)
    return answer


def main():
    puzzle = Puzzle(year=2023, day=4)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 4), {})
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
