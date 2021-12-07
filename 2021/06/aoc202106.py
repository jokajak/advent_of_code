"""AoC 6, 2021"""

# Standard library imports
import pathlib
import sys
from dataclasses import dataclass, field
from aocd import data, submit


@dataclass
class LanternFishList:
    fish: list[int]
    waiting_fish: list[int]
    new_fish: list[int]
    born_fish: int = 0
    current_day: int = 0
    fish_born_yesterday: int = 0
    iteration: int = 0
    fish_reproduction_cycle: int = 7

    def __init__(self, input: list) -> None:
        """Initialize lanternfish object."""
        self.fish = [0] * 8  # A fish creates a new fish every 7 days
        self.waiting_fish = [0] * 3  # Two day delay for fish
        self.new_fish = [0] * 7
        for fish in input:
            self.fish[fish] += 1

    def __repr__(self) -> str:
        ret = []
        ret.append(",".join([str(n) for n in self.fish]))
        new_line = []
        for _ in range(self.current_day):
            new_line.append(" ")
        new_line.append("^")
        ret.append(" ".join(new_line))
        new_fish_day = (self.current_day - 2) % len(self.fish)
        new_line = []
        for _ in range(new_fish_day):
            new_line.append(" ")
        new_line.append("*")
        ret.append(" ".join(new_line))
        return "\n".join(ret)

    def aoc_output(self) -> str:
        ret = []
        for index, value in enumerate(self.fish):
            days_to_new_fish = (len(self.fish) - self.current_day + index) % len(
                self.fish
            )
            if value > 0:
                ret.extend([days_to_new_fish] * value)
        for index, value in enumerate(self.new_fish):
            days_to_new_fish = len(self.fish) + index
            if value > 0:
                ret.extend([days_to_new_fish] * value)
        ret.extend([len(self.fish) + 1] * self.fish_born_yesterday)
        ret = sorted(ret)
        ret = [",".join([str(v) for v in ret])]
        return f"{self.iteration}: " + ",".join(ret)

    def new_day(self, new_fish: int = 0) -> int:
        self.iteration += 1
        fish_born_today = self.fish[0]
        current_fish = [count for count in self.fish]
        for index in range(len(self.fish)-1):
            self.fish[index] = current_fish[index + 1]
        self.fish[6] += fish_born_today
        self.fish[-1] = new_fish
        return fish_born_today

    def end_day(self) -> None:
        pass

    @property
    def total_fish(self) -> int:
        return sum(self.fish)


def parse(puzzle_input):
    """Parse input"""
    return [int(n) for n in puzzle_input.split(",")]


def part1(input_data, days: int = 80):
    """Solve part 1.

    Initial state: 3,4,3,1,2 -> 1,2,3,3,4
    Day 1: 2,3,2,0,1 -> 0,1,2,2,3
    Day 2: 1,2,1,6,0,8 -> 0,1,1,2,6,8
    Day 3: 0,1,0,5,6,7,8 -> 0,0,1,5,6,7,8
    Day 4: 6,0,6,4,5,6,7,8,8 -> 0,4,5,6,6,6,7,8,8
    Day 5: 5,6,5,3,4,5,6,7,7,8 -> 3,4,5,5,5,6,6,7,7,8
    """
    lantern_fish = LanternFishList(input_data)
    fish_born = 0
    for day in range(days):
        fish_born = lantern_fish.new_day(fish_born)
    return lantern_fish.total_fish + fish_born


def part2(input_data):
    """Solve part 2"""
    return part1(input_data, days=256)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    input_data = parse(puzzle_input)
    import time
    tic = time.perf_counter()
    solution1 = part1(input_data)
    toc = time.perf_counter()
    solution2 = part2(input_data)
    tick = time.perf_counter()
    print(f"Complete in {tic - toc:0.7f} seconds\nComplete in {toc - tick:0.7f} seconds")

    return solution1, solution2


if __name__ == "__main__":
    answer_a, answer_b = solve(puzzle_input=data)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
