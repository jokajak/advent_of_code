#!/usr/bin/env python
"""Parsers for various AoC problems"""


def str_to_list(num: str) -> list:
    """Convert an encoded list to a list.

    From 2021 day 18
    """
    ret = []
    current_number = ""
    for char in num:
        if char == "[":
            ret.append(char)
        elif char in ",]":
            if current_number != "":
                ret.append(int(current_number))
                current_number = ""
            if char == "]":
                ret.append(char)
        elif char in "0123456789":
            current_number += char
        else:
            raise ValueError("Unknown character")
    return ret


def str_to_list_2022_13(num: str) -> list:
    """Convert an encoded list to a list.

    From 2022 day 13
    """
    ret = []
    current_number = ""
    for char in num:
        if char == "[":
            ret.append(char)
        elif char in ",]":
            if current_number != "":
                ret.append(int(current_number))
                current_number = ""
            if char == "]":
                ret.append(char)
        elif char in "0123456789":
            current_number += char
        else:
            raise ValueError("Unknown character")
    return ret
