#!/usr/bin/env python
"""Solutions for AoC 21, 2022."""
# Created: 2022-12-25 20:25:51.388619

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import inspect, print
from rich.progress import track


def parse(input_data):
    """Transform the data"""
    ret = {}
    numeric_monkeys = {}
    for line in input_data.splitlines():
        monkey, value = line.split(": ")
        value = value.split(" ")
        if len(value) == 1:
            value = int(value[0])
        else:
            left, operand, right = value
            # If we've already seen both monkeys, go ahead and calculate the value

            if left in numeric_monkeys and right in numeric_monkeys:
                left = int(ret[left])
                right = int(ret[right])
                match operand:
                    case "+":
                        value = left + right
                    case "-":
                        value = left - right
                    case "/":
                        value = int(left / right)
                    case "*":
                        value = left * right
                value = int(value)
        if type(value) == int:
            numeric_monkeys[monkey] = value
        ret[monkey] = value
    return ret, numeric_monkeys


def reduce_monkeys(ms, numeric_monkeys):
    ret = {}
    num_monkeys = numeric_monkeys.copy()
    for monkey, value in ms.items():
        if type(value) == int:
            num_monkeys[monkey] = value
            ret[monkey] = value
            continue
        left, operand, right = value
        if left in num_monkeys and right in num_monkeys:
            left = int(num_monkeys[left])
            right = int(num_monkeys[right])
            match operand:
                case "+":
                    value = left + right
                case "-":
                    value = left - right
                case "/":
                    value = int(left / right)
                case "*":
                    value = left * right
        if type(value) == int:
            num_monkeys[monkey] = value
        ret[monkey] = value
    return ret, num_monkeys


def solve_part_one(input_data):
    """Solve part one.

        # --- Day 21: Monkey Math ---
    The [monkeys](11) are back! You're worried they're going to try to
    steal your stuff again, but it seems like they're just holding their
    ground and making various monkey noises at you.
    Eventually, one of the elephants realizes you don't speak monkey and
    comes over to interpret. As it turns out, they overheard you talking
    about trying to find the grove; they can show you a shortcut if you
    answer their *riddle*.
    Each monkey is given a *job*: either to *yell a specific number* or to
     *yell the result of a math operation*. All of the number-yelling
    monkeys know their number from the start; however, the math operation
    monkeys need to wait for two other monkeys to yell a number, and those
     two other monkeys might *also* be waiting on other monkeys.
    Your job is to *work out the number the monkey named `root` will yell*
     before the monkeys figure it out themselves.
    For example:
    ```
    root: pppw + sjmn
    dbpl: 5
    cczh: sllz + lgvd
    zczc: 2
    ptdq: humn - dvpt
    dvpt: 3
    lfqf: 4
    humn: 5
    ljgn: 2
    sjmn: drzm * dbpl
    sllz: 4
    pppw: cczh / lfqf
    lgvd: ljgn * ptdq
    drzm: hmdt - zczc
    hmdt: 32
    ```
    Each line contains the name of a monkey, a colon, and then the job of
    that monkey:
     - A lone number means the monkey's job is simply to yell that number.
     - A job like `aaaa + bbbb` means the monkey waits for monkeys `aaaa`
    and `bbbb` to yell each of their numbers; the monkey then yells the
    sum of those two numbers.
     - `aaaa - bbbb` means the monkey yells `aaaa`'s number minus `bbbb`'s
     number.
     - Job `aaaa * bbbb` will yell `aaaa`'s number multiplied by `bbbb`'s
    number.
     - Job `aaaa / bbbb` will yell `aaaa`'s number divided by `bbbb`'s
    number.
    So, in the above example, monkey `drzm` has to wait for monkeys `hmdt`
     and `zczc` to yell their numbers. Fortunately, both `hmdt` and `zczc`
     have jobs that involve simply yelling a single number, so they do
    this immediately: `32` and `2`. Monkey `drzm` can then yell its number
     by finding `32` minus `2`: `30`.
    Then, monkey `sjmn` has one of its numbers (`30`, from monkey `drzm`),
     and already has its other number, `5`, from `dbpl`. This allows it to
     yell its own number by finding `30` multiplied by `5`: `150`.
    This process continues until `root` yells a number: `152`.
    However, your actual situation involves *considerably more monkeys*.
    *What number will the monkey named `root` yell?*
    """
    monkeys, numeric_monkeys = input_data

    steps = 50
    r = "c"
    for _ in track(range(steps), description="Following the monkeys"):
        monkeys, numeric_monkeys = reduce_monkeys(monkeys, numeric_monkeys)
        if r != "c":
            r = input("Continue? ")
        if "root" in numeric_monkeys:
            break

    answer = monkeys.get("root")
    return answer


def solve_part_two(input_data):
    """Solve part two.

    Due to some kind of monkey-elephant-human mistranslation, you seem to have misunderstood a few key details about the riddle.

    First, you got the wrong job for the monkey named root; specifically, you got the wrong math operation. The correct operation for monkey root should be =, which means that it still listens for two numbers (from the same two monkeys as before), but now checks that the two numbers match.

    Second, you got the wrong monkey for the job starting with humn:. It isn't a monkey - it's you. Actually, you got the job wrong, too: you need to figure out what number you need to yell so that root's equality check passes. (The number that appears after humn: in your input is now irrelevant.)

    In the above example, the number you need to yell to pass root's equality test is 301. (This causes root to get the same number, 150, from both of its monkeys.)

    What number do you yell to pass root's equality test?
    """
    orig_monkeys, numeric_monkeys = input_data
    monkeys = orig_monkeys.copy()
    num_monkeys = numeric_monkeys.copy()

    # Calculate number of steps
    steps = 50
    for _ in track(range(steps), description="Following the monkeys"):
        monkeys, num_monkeys = reduce_monkeys(monkeys, num_monkeys)
        if "root" in num_monkeys:
            step_counter = _
            break
    print(f"Reduced in {step_counter} steps")

    def reverse_operations(monkeys, monkey, steps=50):
        # First, find the monkey that depends on humn
        operations = []
        unknown_monkey = "humn"
        for _ in range(steps):
            for m, v in monkeys.items():
                if type(v) == int:
                    continue
                left, operand, right = v
                if left == unknown_monkey:
                    # this is the "easy" way
                    if right in monkeys and type(monkeys[right]) == int:
                        right = monkeys[right]
                    operations.append((operand, right))
                    unknown_monkey = m
                elif right == unknown_monkey:
                    if left in monkeys and type(monkeys[left]) == int:
                        left = monkeys[left]
                    operations.append((left, operand))
                    unknown_monkey = m
                else:
                    continue
        return operations

    def solve_operations(operations, val):
        result = val
        for entry in reversed(operations):
            left, right = entry
            print(result, entry)
            match left:
                case "+":
                    result -= right
                case "-":
                    result += right
                case "*":
                    result = int(result / right)
                case "/":
                    result *= right
                case "=":
                    result = result
                case _:
                    match right:
                        # 4 + x = y
                        # x = y - 4
                        case "+":
                            result -= left
                        # 4 - x = y
                        # 4 - y = x
                        case "-":
                            result = left - result
                        # 4 * x = y
                        # x = y / 4
                        case "*":
                            result = int(result / left)
                        # 4 / x = y
                        # x = 4 / y
                        case "/":
                            result = int(left / result)
        return result

    monkeys = orig_monkeys.copy()
    monkeys["humn"] = ("x", "+", "y")
    num_monkeys = numeric_monkeys.copy()
    # Remove humn from numeric monkeys
    num_monkeys.pop("humn", None)
    for _ in range(step_counter):
        monkeys, num_monkeys = reduce_monkeys(monkeys, num_monkeys)
    left, operand, right = monkeys["root"]
    monkeys["root"] = (left, "=", right)
    if right in num_monkeys:
        print(f"Left: {left}")
        operations = reverse_operations(monkeys, left, steps=step_counter + 1)
        answer = solve_operations(operations, monkeys[right])
    elif left in num_monkeys:
        print(f"Right: {right}")
        operations = reverse_operations(monkeys, right, steps=step_counter + 1)
        answer = solve_operations(operations, monkeys[left])
    return answer


def main():
    puzzle = Puzzle(year=2022, day=21)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2022).get((2022, 21), {})
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
