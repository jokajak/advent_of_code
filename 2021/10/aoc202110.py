"""AoC 10, 2021"""

# Standard library imports
import pathlib
import sys

from aocd import data as input_data, submit
from collections import Counter, deque


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.splitlines()


class SyntaxValidator:
    def __init__(self, entry: list):
        self.illegal_brackets = {")": 0, "]": 0, "}": 0, ">": 0}
        open_brackets = []
        for bracket in entry:
            if bracket in "([{<":
                open_brackets.append(bracket)
            elif bracket in ">}])":
                opening_bracket = open_brackets.pop()
                matching_bracket = (
                    (opening_bracket == "(" and bracket == ")")
                    or (opening_bracket == "[" and bracket == "]")
                    or (opening_bracket == "{" and bracket == "}")
                    or (opening_bracket == "<" and bracket == ">")
                )

                if matching_bracket or self.syntax_score != 0:
                    continue
                else:
                    self.illegal_brackets[bracket] += 1
        closing_brackets = deque()
        matching_brackets = {
            "(": ")",
            "{": "}",
            "[": "]",
            "<": ">"
        }
        for bracket in open_brackets:
          closing_brackets.insert(0, matching_brackets[bracket])
        self.closing_score = self.score_closing_brackets(closing_brackets)

    @property
    def syntax_score(self) -> int:
        bracket_values = {")": 3, "]": 57, "}": 1197, ">": 25137}
        illegal_brackets = self.illegal_brackets
        return (
            illegal_brackets[")"] * bracket_values[")"]
            + illegal_brackets["}"] * bracket_values["}"]
            + illegal_brackets["]"] * bracket_values["]"]
            + illegal_brackets[">"] * bracket_values[">"]
        )

    @staticmethod
    def score_closing_brackets(brackets: list) -> int:
        """Generate score for closing brackets.

        The score is determined by considering the completion string character-by-character. Start with a total score of
        0. Then, for each character, multiply the total score by 5 and then increase the total score by the point value
        given for the character in the following table:

        ): 1 point.
        ]: 2 points.
        }: 3 points.
        >: 4 points.

        """
        score = 0
        bracket_values = {")": 1, "]": 2, "}": 3, ">": 4}
        for bracket in brackets:
            score *= 5
            score += bracket_values[bracket]
        return score

def part1(data):
    """Solve part 1.
    The navigation subsystem syntax is made of several lines containing chunks. There are one or more chunks on each
    line, and chunks contain zero or more other chunks. Adjacent chunks are not separated by any delimiter; if one chunk
    stops, the next chunk (if any) can immediately start. Every chunk must open and close with one of four legal pairs
    of matching characters:

    If a chunk opens with (, it must close with ). If a chunk opens with [, it must close with ]. If a chunk opens with
    {, it must close with }. If a chunk opens with <, it must close with >. So, () is a legal chunk that contains no
    other chunks, as is []. More complex but valid chunks include ([]), {()()()}, <([{}])>, [<>({}){}[([])<>]], and even
    (((((((((()))))))))).

    Some lines are incomplete, but others are corrupted. Find and discard the corrupted lines first.

    A corrupted line is one where a chunk closes with the wrong character - that is, where the characters it opens and
    closes with do not form one of the four legal pairs listed above.
    """
    total_score = 0
    for entry in data:
        validator = SyntaxValidator(entry)
        #print(f"{entry}: {validator.syntax_score}")
        total_score += validator.syntax_score

    return total_score


def part2(data):
    """Solve part 2.

    Now, discard the corrupted lines. The remaining lines are incomplete.

    Incomplete lines don't have any incorrect characters - instead, they're missing some closing characters at the end
    of the line. To repair the navigation subsystem, you just need to figure out the sequence of closing characters that
    complete all open chunks in the line.

    You can only use closing characters (), ], }, or >), and you must add them in the correct order so that only legal
    pairs are formed and all chunks end up closed.

    In the example above, there are five incomplete lines:

    [({(<(())[]>[[{[]{<()<>> - Complete by adding }}]])})]. [(()[<>])]({[<{<<[]>>( - Complete by adding )}>]}).
    (((({<>}<{<{<>}{[]{[]{} - Complete by adding }}>}>)))). {<[[]]>}<{[{[{[]{()[[[] - Complete by adding ]]}}]}]}>.
    <{([{{}}[<[[[<>{}]]]>[]] - Complete by adding ])}>. Did you know that autocomplete tools also have contests? It's
    true! The score is determined by considering the completion string character-by-character. Start with a total score
    of 0. Then, for each character, multiply the total score by 5 and then increase the total score by the point value
    given for the character in the following table:

    ): 1 point. ]: 2 points. }: 3 points.
    >: 4 points.


    Autocomplete tools are an odd bunch: the winner is found by sorting all of the scores and then taking the middle
    score. (There will always be an odd number of scores to consider.) In this example, the middle score is 288957
    because there are the same number of scores smaller and larger than it.
    """
    closing_scores = []
    for entry in data:
        validator = SyntaxValidator(entry)
        # print(f"{entry}: {validator.syntax_score}")
        if validator.syntax_score != 0:
            continue
        closing_scores.append(validator.closing_score)

    closing_scores = sorted(closing_scores)
    assert len(closing_scores) % 2 == 1

    return closing_scores[int((len(closing_scores) - 1)/2)]



def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    answer_a, answer_b = solve(puzzle_input=input_data)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
