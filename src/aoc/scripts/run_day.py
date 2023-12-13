#!/usr/bin/env python3

import os
import datetime
import argparse


def run_script(year, day, run_test=False):
    # Construct the path for the script and test file
    script_path = f"./src/aoc/y{year}/d{day}.py"
    test_path = f"./src/aoc/tests/y{year}/test_{day}.py"

    # Check if --test is provided and the test file exists
    if run_test and os.path.exists(test_path):
        # Run pytest for the test file
        os.system(f"pytest {test_path}")
    elif run_test:
        print(f"Test file for year {year}, day {day} not found.")
    elif os.path.exists(script_path):
        # Run the script
        os.system(f"python {script_path}")
    else:
        print(f"Script for year {year}, day {day} not found.")


def main():
    # Get the current year and day
    current_year = datetime.datetime.now().year
    current_day = datetime.datetime.now().day

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run Advent of Code script and pytest for a specific year and day."
    )
    parser.add_argument(
        "--year",
        type=int,
        default=current_year,
        help="Specify the year (default is current year)",
    )
    parser.add_argument(
        "--day",
        type=int,
        default=current_day,
        help="Specify the day (default is current day)",
    )
    parser.add_argument(
        "--test", action="store_true", help="Run pytest for the corresponding test file"
    )

    args = parser.parse_args()

    # Run the script and pytest based on the provided year, day, and test flag
    run_script(args.year, args.day, args.test)


if __name__ == "__main__":
    main()
