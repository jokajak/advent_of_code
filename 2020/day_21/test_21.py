#!/usr/bin/env python3

from collections import defaultdict, Counter

import parse
import pytest

ALLERGENS_PARSE_STRING = "{foods} (contains {allergens})"


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            [
                "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
                "trh fvjkl sbzzf mxmxvkd (contains dairy)",
                "sqjhc fvjkl (contains soy)",
                "sqjhc mxmxvkd sbzzf (contains fish)",
            ],
            5,
        ),
    ],
)
def test_find_safe_food(input, expected):
    assert find_safe_food(input) == expected


def find_safe_food(input):
    all_foods = Counter()
    food_allergens = {}
    for line in input:
        parsed_string = parse.parse(ALLERGENS_PARSE_STRING, line)
        # No allergens
        if parsed_string is None:
            # Update no allergen foods
            foods = line.split(" ")
            all_foods.update(foods)
            for food in foods:
                food_allergens[food] = set()
        # Has allergens
        else:
            allergens = parsed_string["allergens"].split(", ")
            foods = set(parsed_string["foods"].split(" "))
            all_foods.update(foods)
            for food in foods:
                if food in food_allergens:
                    food_allergens[food].intersection_update(set(allergens))
                else:
                    food_allergens[food] = set(allergens)
    for food in food_allergens:
        if len(food_allergens[food]) > 0:
            all_foods[food] = 0
    # Need to count the recipes with the safe foods
    safe_foods = 0

    return safe_foods
