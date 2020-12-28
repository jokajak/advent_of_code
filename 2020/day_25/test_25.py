#!/usr/bin/env python

import pytest


@pytest.mark.parametrize(
    "subject_number, loop_size, expected",
    [
        (7, 8, 5764801),
        (7, 11, 17807724),
        (17807724, 8, 14897079),
        (5764801, 11, 14897079),
    ]
)
def test_transform_number(subject_number, loop_size, expected):
    assert transform_number(subject_number=subject_number, loop_size=loop_size) == expected


def transform_number(*, subject_number, loop_size):
    val = 1
    for _ in range(loop_size):
        val = val * subject_number
        val = val % 20201227
    return val


def main(input, public_key):
    # From the cryptographic instructions description the subject number is always 7
    # We know that the public key for the card is between 1 and 20201227 because of the modulus
    # If we loop N times between 1 and 20201227 and the value becomes what we want then we know the loop size
    value = 1
    subject_number = 7
    for i in range(1, 20201227):
        value = (value * subject_number) % 20201227
        if value == input:
            break
    print(i)
    # Calculate encryption key
    print(transform_number(subject_number=public_key, loop_size=i))


if __name__ == "__main__":
    main(17807724, 5764801)
    main(1965712, 19072108)
