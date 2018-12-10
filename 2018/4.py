#!/usr/bin/env python3
"""
Advent of Code 2018, Day 4
"""

__author__ = "Josh"
__version__ = "0.1.0"
__license__ = "GPLv3"

import argparse
import logging
import logzero
from collections import defaultdict
from logzero import logger
from datetime import datetime, timedelta


def parse_line(line):
    guard_id = None
    awake = True
    time_entry = line.split(']')[0]
    line = line.strip()
    if (line.endswith('falls asleep')):
        awake = False
    if ('Guard' in line):
        guard_id = line.split(' ')[3]
        guard_id = guard_id.split('#')[1]
    timestamp = datetime.strptime(time_entry, '[%Y-%m-%d %H:%M')
    return timestamp, guard_id, awake

def main(args):
    """ Main entry point of the app """
    if (0 == args.verbose):
        logzero.loglevel(logging.INFO)
    elif (1 == args.verbose):
        logzero.loglevel(logging.DEBUG)

    entries = []
    events = []
    for line in args.input.readlines():
        line = line.strip()
        entries.append(line)
        events.append(parse_line(line))
        logger.debug(parse_line(line))
    events.sort(key=lambda tup: tup[0])
    is_asleep = False
    guard_sleep_times = defaultdict(list)
    current_guard = None
    last_timestamp = None
    for event in events:
        logger.debug(event)
        timestamp, new_guard_id, awake = event
        if new_guard_id and current_guard != new_guard_id:
            logger.debug('New guard')
            if current_guard and is_asleep:
                guard_sleep_times[current_guard].append((last_timestamp, timestamp))
            last_timestamp = timestamp
            is_asleep = False
            current_guard = new_guard_id
            continue
        if is_asleep and awake:
            logger.debug('Guard woke up')
            guard_sleep_times[current_guard].append((last_timestamp, timestamp))
            is_asleep = False
            continue
        if not awake:
            logger.debug('Guard went to sleep')
            last_timestamp = timestamp
            is_asleep = True
    max_sleep = timedelta()
    sleepy_guard_id = 0
    guard_minutes = [{} for i in range(0,60)]
    for guard, sleep_times in guard_sleep_times.items():
        logger.debug(sleep_times)
        sleep_time = timedelta()
        for start, stop in sleep_times:
            sleep_time += stop - start
            while start < stop:
                start_minute = start.minute
                logger.debug('{} {}'.format(guard, start_minute))
                if guard_minutes[start_minute]:
                    pass
                else:
                    guard_minutes[start_minute] = {}
                if guard not in guard_minutes[start_minute]:
                    guard_minutes[start_minute][guard] = 0
                guard_minutes[start_minute][guard] += 1
                logger.debug(guard_minutes)
                start += timedelta(minutes=1)
        logger.debug(sleep_time)
        if sleep_time > max_sleep:
            max_sleep = sleep_time
            sleepy_guard_id = guard
    logger.debug(sleepy_guard_id)
    minutes = defaultdict(int)
    for sleep_times in guard_sleep_times[sleepy_guard_id]:
        start, stop = sleep_times
        start_minute = start.minute
        while start_minute < stop.minute:
            minutes[start_minute] += 1
            start_minute += 1
    logger.debug(minutes)
    max_minute, max_count = 0, 0
    for minute, count in minutes.items():
        if count> max_count:
            max_minute = minute
            max_count = count
    logger.info(max_minute*int(sleepy_guard_id))
    max_minute, max_count, max_guard_id = 0, 0, 0
    for minute, entries in enumerate(guard_minutes):
        for guard, count in entries.items():
            if count > max_count:
                max_minute = minute
                max_count = count
                max_guard_id = guard
    logger.debug(guard_minutes)
    logger.debug(max_guard_id)
    logger.info(int(max_guard_id) * max_minute)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument(
        "input",
        type=argparse.FileType('r'),
        help="Required positional argument"
    )

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
