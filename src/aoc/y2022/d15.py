#!/usr/bin/env python
"""Solutions for AoC 15, 2022."""
# Created: 2022-12-15 08:33:55.210123

from functools import cache

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import inspect, print
from rich.progress import track

from aoc.utils.pathfinding import GridLocation, SquareGrid, draw_grid


def inside_sensor(center: GridLocation, point: GridLocation, reach: int) -> bool:
    """Calculate if a coordinate is reachable from a sensor"""
    dx = center[0] - point[0]
    dy = center[1] - point[1]
    distance = abs(dx) + abs(dy)
    return distance <= reach


class TunnelSystem(SquareGrid):
    """Represent a tunnel system"""

    def __init__(
        self,
        width: int,
        height: int,
        sensors: list[GridLocation],
        beacons: list[GridLocation],
        sensor_distances: dict[GridLocation],
    ):
        self.sensors = sensors or []
        self.beacons = beacons or []
        self.width = width
        self.height = height
        self.walls: list[GridLocation] = []
        self.covered: list[GridLocation] = []
        self.sensor_distances: dict[GridLocation] = sensor_distances or {}

    def sensor_reaches(self, sensor: GridLocation, row: int) -> bool:
        """Calculate if a sensor can reach a row"""
        radius = self.sensor_distances.get(sensor)
        sensor_x, sensor_y = sensor
        return inside_sensor(sensor, (sensor_x, row), radius)

    @staticmethod
    def parse_sensor_beacon(line: str) -> list[GridLocation]:
        """Parse a sensor beacon pair string.

        Sensor at x=2, y=18: closest beacon is at x=-2, y=15
          0     1  2    3       4       5    6  7   8     9
        """
        sensor_x = int(line[2].split("=")[1].split(",")[0])
        sensor_y = int(line[3].split("=")[1].split(":")[0])
        beacon_x = int(line[8].split("=")[1].split(",")[0])
        beacon_y = int(line[9].split("=")[1])
        distance = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
        return (sensor_x, sensor_y), (beacon_x, beacon_y), distance

    def draw(self, sensor=None):
        min_x = min(x for x, _ in self.beacons)
        min_x = min(min_x, min(x for x, _ in self.sensors))
        min_y = min(y for _, y in self.beacons)
        min_y = min(min_y, min(y for _, y in self.sensors))
        if sensor is None:
            letters = {(x - min_x, y - min_y): "#" for x, y in self.covered}
        else:
            x, y = sensor
            radius = self.sensor_distances.get(sensor)
            top = y - radius
            bottom = y + radius
            left = x - radius
            right = x + radius
            print(f"{top} {bottom} {left} {right} {sensor} {radius}")
            letters = {}
            for y in range(top, bottom + 1):
                for x in range(left, right + 1):
                    if inside_sensor(sensor, (x, y), radius):
                        letters[(x - min_x, y - min_y)] = "#"

        letters.update({(x - min_x, y - min_y): "B" for x, y in self.beacons})
        letters.update({(x - min_x, y - min_y): "S" for x, y in self.sensors})

        draw_grid(
            self,
            letter=letters,
            trim=True,
            blank=False,
            draw_axis=True,
        )

    def get_row(self, row: int) -> str:
        """Return a string rendering of a row"""
        ret = []
        for x in range(self.width):
            r = "."
            if (x, row) in self.sensors:
                r = "S"
            elif (x, row) in self.beacons:
                r = "B"
            elif (x, row) in self.covered:
                r = "#"
            ret.append(r)
        return "".join(ret)


def parse(input_data):
    """Transform the data.

    Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    """
    sensors: list[GridLocation] = []
    beacons: list[GridLocation] = []
    sensor_distances: dict[GridLocation] = {}
    min_x = min_y = float("inf")
    max_x = max_y = 0
    for line in input_data.splitlines():
        line = line.strip().split(" ")
        sensor, beacon, distance = TunnelSystem.parse_sensor_beacon(line)
        sensor_x, sensor_y = sensor
        beacon_x, beacon_y = beacon
        sensors.append(sensor)
        beacons.append(beacon)
        sensor_distances[sensor] = distance
        min_x = min(min_x, sensor_x, beacon_x)
        min_y = min(min_y, sensor_y, beacon_y)
        max_x = max(max_x, sensor_x, beacon_x)
        max_y = max(max_y, sensor_y, beacon_y)

    # Normalize coordinates to start at 0
    # -2 - - 2 = 0
    # 2 - -2 = 4
    # beacons = [(x - min_x, y - min_y) for x, y in beacons]
    # sensors = [(x - min_x, y - min_y) for x, y in sensors]
    # sensor_distances = {(k[0], k[1]): v for k, v in sensor_distances.items()}

    ret = TunnelSystem(
        width=abs(max_x - min_x),
        height=abs(max_y - min_y),
        sensors=sensors,
        beacons=beacons,
        sensor_distances=sensor_distances,
    )
    return ret


def calculate_range(sensor, y, reach):
    """Calculate the range of a sensor covering a row.

    The row will intersect 2 points around the sensor
    y = mx + b
    Given 2 points, calculate m and b
    m is either -1 or 1 based on direction
    b = y - mx
    """
    s_x, s_y = sensor
    top = (s_x, s_y - reach)
    bottom = (s_x, s_y + reach)
    y_pos = top if y < s_y else bottom

    # x increases as y approaches y_pos
    # y = +1 x + b
    # b = y - x
    left_b = y_pos[1] - y_pos[0]
    # x decreases as y approaches y_pos
    # y = -1 x + b
    # b = y + x
    right_b = y_pos[1] + y_pos[0]
    # y = -1 x + b => y + x = b => x = b - y
    right_x = right_b - y
    # y = 1 x + b => y - b = x
    left_x = y - left_b
    if y < s_y:
        return right_x, left_x
    else:
        return left_x, right_x


# From ChatGPT
def manhattan_intersection(
    x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int
) -> bool:
    """
    Calculates if two line segments intersect in Manhattan geometry.

    The line segments are defined as pairs of points (x1, y1, x2, y2) and (x3, y3, x4, y4).

    Returns:
        True if the line segments intersect, False otherwise.
    """
    # Check if any of the endpoints of the first line segment lie on the second line segment
    if (min(x3, x4) <= x1 <= max(x3, x4)) and (min(y3, y4) <= y1 <= max(y3, y4)):
        return True
    if (min(x3, x4) <= x2 <= max(x3, x4)) and (min(y3, y4) <= y2 <= max(y3, y4)):
        return True

    # Check if any of the endpoints of the second line segment lie on the first line segment
    if (min(x1, x2) <= x3 <= max(x1, x2)) and (min(y1, y2) <= y3 <= max(y1, y2)):
        return True
    if (min(x1, x2) <= x4 <= max(x1, x2)) and (min(y1, y2) <= y4 <= max(y1, y2)):
        return True

    return False


def solve_part_one(input_data, y=2000000):
    """Solve part one.

        # --- Day 15: Beacon Exclusion Zone ---
    You feel the ground rumble again as the distress signal leads you to a
     large network of subterranean tunnels. You don't have time to search
    them all, but you don't need to: your pack contains a set of
    deployable *sensors* that you imagine were originally built to locate
    lost Elves.
    The sensors aren't very powerful, but that's okay; your handheld
    device indicates that you're close enough to the source of the
    distress signal to use them. You pull the emergency sensor system out
    of your pack, hit the big button on top, and the sensors zoom off down
     the tunnels.
    Once a sensor finds a spot it thinks will give it a good reading, it
    attaches itself to a hard surface and begins monitoring for the
    nearest signal source *beacon*. Sensors and beacons always exist at
    integer coordinates. Each sensor knows its own position and can
    *determine the position of a beacon precisely*; however, sensors can
    only lock on to the one beacon *closest to the sensor* as measured by
    the [Manhattan
    distance](https://en.wikipedia.org/wiki/Taxicab_geometry). (There is
    never a tie where two beacons are the same distance to a sensor.)
    It doesn't take long for the sensors to report back their positions
    and closest beacons (your puzzle input). For example:
    ```
    Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    Sensor at x=9, y=16: closest beacon is at x=10, y=16
    Sensor at x=13, y=2: closest beacon is at x=15, y=3
    Sensor at x=12, y=14: closest beacon is at x=10, y=16
    Sensor at x=10, y=20: closest beacon is at x=10, y=16
    Sensor at x=14, y=17: closest beacon is at x=10, y=16
    Sensor at x=8, y=7: closest beacon is at x=2, y=10
    Sensor at x=2, y=0: closest beacon is at x=2, y=10
    Sensor at x=0, y=11: closest beacon is at x=2, y=10
    Sensor at x=20, y=14: closest beacon is at x=25, y=17
    Sensor at x=17, y=20: closest beacon is at x=21, y=22
    Sensor at x=16, y=7: closest beacon is at x=15, y=3
    Sensor at x=14, y=3: closest beacon is at x=15, y=3
    Sensor at x=20, y=1: closest beacon is at x=15, y=3
    ```
    So, consider the sensor at `2,18`; the closest beacon to it is at
    `-2,15`. For the sensor at `9,16`, the closest beacon to it is at
    `10,16`.
    Drawing sensors as `S` and beacons as `B`, the above arrangement of
    sensors and beacons looks like this:
    ```
                   1    1    2    2
         0    5    0    5    0    5
     0 ....S.......................
     1 ......................S.....
     2 ...............S............
     3 ................SB..........
     4 ............................
     5 ............................
     6 ............................
     7 ..........S.......S.........
     8 ............................
     9 ............................
    10 ....B.......................
    11 ..S.........................
    12 ............................
    13 ............................
    14 ..............S.......S.....
    15 B...........................
    16 ...........SB...............
    17 ................S..........B
    18 ....S.......................
    19 ............................
    20 ............S......S........
    21 ............................
    22 .......................B....
    ```
    This isn't necessarily a comprehensive map of all beacons in the area,
     though. Because each sensor only identifies its closest beacon, if a
    sensor detects a beacon, you know there are no other beacons that
    close or closer to that sensor. There could still be beacons that just
     happen to not be the closest beacon to any sensor. Consider the
    sensor at `8,7`:
    ```
                   1    1    2    2
         0    5    0    5    0    5
    -2 ..........#.................
    -1 .........###................
     0 ....S...#####...............
     1 .......#######........S.....
     2 ......#########S............
     3 .....###########SB..........
     4 ....#############...........
     5 ...###############..........
     6 ..#################.........
     7 .#########S#######S#........
     8 ..#################.........
     9 ...###############..........
    10 ....B############...........
    11 ..S..###########............
    12 ......#########.............
    13 .......#######..............
    14 ........#####.S.......S.....
    15 B........###................
    16 ..........#SB...............
    17 ................S..........B
    18 ....S.......................
    19 ............................
    20 ............S......S........
    21 ............................
    22 .......................B....
    ```
    This sensor's closest beacon is at `2,10`, and so you know there are
    no beacons that close or closer (in any positions marked `#`).
    None of the detected beacons seem to be producing the distress signal,
     so you'll need to *work out* where the distress beacon is by working
    out where it *isn't*. For now, keep things simple by counting the
    positions where a beacon cannot possibly be along just a single row.
    So, suppose you have an arrangement of beacons and sensors like in the
     example above and, just in the row where `y=10`, you'd like to count
    the number of positions a beacon cannot possibly exist. The coverage
    from all sensors near that row looks like this:
    ```
                     1    1    2    2
           0    5    0    5    0    5
     9 ...#########################...
    10 ..####B######################..
    11 .###S#############.###########.
    ```
    In this example, in the row where `y=10`, there are `26` positions
    where a beacon cannot be present.
    Consult the report from the sensors you just deployed. *In the row
    where `y=2000000`, how many positions cannot contain a beacon?*
    """
    tunnel = input_data

    blocked = {}

    sensors = []
    for sensor in track(tunnel.sensors, description="Checking sensors"):
        radius = tunnel.sensor_distances[sensor]
        sensor_x, sensor_y = sensor
        if tunnel.sensor_reaches(sensor, y):
            sensors.append(sensor)
            left_x, right_x = calculate_range(sensor, y, radius)
            print(f"{sensor}: {left_x}, {right_x}")
            for x in range(left_x, right_x):
                tunnel.covered.append((x, y))
                blocked[x] = True
            # left = sensor_x - radius
            # right = sensor_x + radius
            # # This is too slow
            # for x in range(left, right):
            #     if inside_sensor(sensor, (x, y), radius):
            #         if not ((x, y) in tunnel.beacons or (x, y) in tunnel.sensors):
            #             tunnel.covered.append((x, y))
            #             blocked[x] = True

    if y == 10:
        tunnel.draw()
        tunnel.draw((8, 7))
        tunnel.draw((0, 11))
        print(sensors)
    answer = len(blocked)
    return answer


def solve_part_two(input_data, search_area=4000000):
    """Solve part two.

    Your handheld device indicates that the distress signal is coming from a beacon nearby. The distress beacon is not detected by any sensor, but the distress beacon must have x and y coordinates each no lower than 0 and no larger than 4000000.

    To isolate the distress beacon's signal, you need to determine its tuning
    frequency, which can be found by multiplying its x coordinate by 4000000
    and then adding its y coordinate.

    In the example above, the search space is smaller: instead, the x and y
    coordinates can each be at most 20. With this reduced search area, there is
    only a single position that could have a beacon: x=14, y=11. The tuning
    frequency for this distress beacon is 56000011.

    Find the only possible position for the distress beacon. What is its tuning frequency?

    """

    tunnel = input_data
    frequency_multiplier = 4000000

    def coords(max_val):
        for x in range(max_val + 1):
            for y in range(max_val + 1):
                yield y, x

    # the point where a beacon can be will be around an intersection between a
    # -1 slope and a +1 slope
    def get_segment_ups(point: GridLocation, reach: int) -> Tuple(int, int):
        x, y = point
        top = y - reach
        bottom = y + reach
        left = x - reach
        right = x + reach
        # x increases as y approaches y_pos
        # y = +1 x + b
        # b = y - x
        left_b = top[1] - top[0]
        # x decreases as y approaches y_pos
        # y = -1 x + b
        # b = y + x
        right_b = y_pos[1] + y_pos[0]
        # y = -1 x + b => y + x = b => x = b - y
        right_x = right_b - y
        # y = 1 x + b => y - b = x
        left_x = y - left_b
        if y < s_y:
            return right_x, left_x
        else:
            return left_x, right_x

        pass

    # This approach is naive and won't work.
    # Takes too long
    # for x, y in track(
    #     coords(search_area),
    #     description="Checking coords",
    #     total=frequency_multiplier * frequency_multiplier,
    # ):
    #     for sensor in tunnel.sensors:
    #         reach = tunnel.sensor_distances.get(sensor)
    #         if inside_sensor(sensor, (x, y), reach):
    #             if x == 14 and y == 11:
    #                 print(f"({x}, {y}) reachable from {sensor}")
    #                 tunnel.draw(sensor=sensor)
    #             break
    #     else:
    #         answer = x * frequency_multiplier + y
    #         return answer
    # else:
    #     print("Whoops")


def main():
    puzzle = Puzzle(year=2022, day=15)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2022).get((2022, 15), {})
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
