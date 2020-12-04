#!/usr/bin/env python

__author__ = "Jokajak"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse
import re


def is_passport_field_valid(field, value):
    """Determine if passport field is valid.

    Args:
        field (string): The passport field
        value (string): The value

    - byr (Birth Year) - four digits; at least 1920 and at most 2002.
    - iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    - eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    - hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    - hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    - ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    - pid (Passport ID) - a nine-digit number, including leading zeroes.
    - cid (Country ID) - ignored, missing or not.
    """
    if field == "byr":
        return int(value) >= 1920 and int(value) <= 2002
    if field == "iyr":
        return int(value) >= 2010 and int(value) <= 2020
    if field == "eyr":
        return int(value) >= 2020 and int(value) <= 2030
    if field == "hcl":
        regex = r"#[0-9a-f]{6}"
        return re.match(regex, value) is not None
    if field == "ecl":
        valid_eye_colors = ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
        return value in valid_eye_colors
    if field == "pid":
        regex = r"^[0-9]{9}$"
        return re.match(regex, value) is not None
    if field == "hgt":
        if value.endswith("in"):
            height = int(value.strip("in"))
            return height >= 59 and height <= 76
        elif value.endswith("cm"):
            height = int(value.strip("cm"))
            return height >= 150 and height <= 193
        return False


def is_valid_passport(passport):
    """Determine if passport is valid

    Args:
        passport (dictionary): All passport fields
    """
    ret = True
    req_fields = (
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid',
    )
    for field in req_fields:
        if field not in passport:
            return False
    for field in req_fields:
        if not is_passport_field_valid(field, passport[field]):
            print("{} is invalid: {}".format(field, passport[field]))
            return False
    return ret


def main(args):
    """Main program flow

    Args:
        args (argparse.Namespace): Parsed arguments
    """
    batch_of_passports = []

    passport = {}
    for line in args.file.readlines():
        line = line.strip("\n")
        if line == "":
            # new passport
            batch_of_passports.append(passport)
            passport = {}
        else:
            print(line)
            fields = line.split(" ")
            for entry in fields:
                field, value = entry.split(":")
                passport[field] = value
    # Add last passport entry
    batch_of_passports.append(passport)

    print(batch_of_passports)
    valid_passports = 0
    for passport in batch_of_passports:
        print("Checking {}".format(passport))
        is_valid = is_valid_passport(passport)
        print(is_valid)
        if is_valid:
            valid_passports += 1
    print(valid_passports)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("--file", type=argparse.FileType("r"), help="Input file", default="2020/inputs/4.test")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)
