#!/usr/bin/env python
"""Solutions for AoC 19, 2023."""
# Created: 2023-12-20 22:45:04.845774

# Standard library imports
from aocd.models import Puzzle, default_user
from rich import print
import ast
import re
from collections import deque, defaultdict


def parse(input_data):
    """Transform the data

    workflows:
    px{a<2006:qkq,m>2090:A,rfg}
    pv{a>1716:R,A}
    lnx{m>1548:A,A}
    rfg{s<537:gd,x>2440:R,A}
    qs{s>3448:A,lnx}
    qkq{x<1416:A,crn}
    crn{x>2662:A,R}
    in{s<1351:px,qqz}
    qqz{s>2770:qs,m<1801:hdj,R}
    gd{a>3333:R,R}
    hdj{m>838:A,pv}

    part ratings:
    {x=787,m=2655,a=1222,s=2876}
    {x=1679,m=44,a=2067,s=496}
    {x=2036,m=264,a=79,s=2244}
    {x=2461,m=1339,a=466,s=291}
    {x=2127,m=1623,a=2188,s=1013}
    """
    workflows_in, ratings_in = input_data.split("\n\n")
    workflows, parts = {}, []
    for workflow_line in workflows_in.splitlines():
        name = workflow_line.split("{")[0]
        workflow_rules = workflow_line.split("{")[1].strip("}").split(",")
        parsed_rules = []
        for rule in workflow_rules:
            try:
                condition, target = rule.split(":")
            except ValueError:
                condition, target = "True", rule
            parsed_rules.append((condition, target))
        workflows[name] = parsed_rules

    for rating_line in ratings_in.splitlines():
        # Replace '=' with ':' and add double quotes around keys
        fixed_string = re.sub(r"(\w+)=", r'"\1":', rating_line)
        part = ast.literal_eval(fixed_string.replace("=", ":"))
        parts.append(part)

    return workflows, parts


def handle_part(part, workflows):
    """Determine if a part is accepted"""
    # simple loop limiter
    max_iters = 10**100
    current_workflow = "in"
    for _ in range(max_iters):
        conditions = workflows[current_workflow]
        for condition, target in conditions:
            ret = eval(condition, part)
            if ret:
                current_workflow = target
                # We had a match, don't have to process any more conditions
                break
        if current_workflow == "A":
            return True
        if current_workflow == "R":
            return False


def solve_part_one(input_data):
    """Solve part one.

    Ultimately, three parts are accepted. Adding up the x, m, a, and s rating for each of the accepted parts gives 7540
    for the part with x=787, 4623 for the part with x=2036, and 6951 for the part with x=2127. Adding all of the ratings
    for all of the accepted parts gives the sum total of 19114.

    Sort through all of the parts you've been given; what do you get if you add together all of the rating numbers for
    all of the parts that ultimately get accepted?
    """
    answer = 0
    workflows, parts = input_data
    accepted = []
    for part in parts:
        ret = handle_part(part, workflows)
        if ret:
            accepted.append(part)
    for part in accepted:
        for component in "xmas":
            if part[component] is not None:
                answer += part[component]
    return answer


def get_approved_paths(workflows):
    max_iters = 10**100
    valid_paths = []
    target_conditions = deque()
    target_conditions.append(("A", ["A"]))
    iters = 0
    while len(target_conditions) > 0 and iters < max_iters:
        iters += 1
        # get the condition we're trying to resolve
        target_condition, path = target_conditions.popleft()
        for workflow, conditions in workflows.items():
            for condition, target in conditions:
                if target == target_condition:
                    new_path = list(path)
                    new_path.append(condition)
                    if workflow == "in":
                        valid_paths.append(new_path)
                    else:
                        target_conditions.append((workflow, new_path))
    return valid_paths


def solve_part_two(input_data):
    """Solve part two."""
    answer = 0
    workflows, _ = input_data
    approved_paths = get_approved_paths(workflows)

    approved_paths = [
        [step for step in path if step not in ("True", "A")] for path in approved_paths
    ]

    print(approved_paths)

    return answer


def main():
    puzzle = Puzzle(year=2023, day=19)
    parsed_data = parse(puzzle.input_data)
    u = default_user()
    stats = u.get_stats(2023).get((2023, 19), {})
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
