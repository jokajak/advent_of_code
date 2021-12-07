"""AoC 4, 2021"""

# Standard library imports
from aocd import data, submit


NONE = object()

class BingoBoard():
    """Bingo Board representation.

    A Bingo Board is composed of multiple cells, each cell has a a value and whether it's been matched.

    Each cell is placed in a grid composed for rows and columns.

    If an entire row or column has all cells matched then the bingo board is a winner
    """

    def __init__(self, input_rows=NONE) -> None:
        self.rows = []
        self.entries = {}
        if input_rows != NONE and isinstance(input_rows, list):
            for row_index in range(len(input_rows)):
                current_row = input_rows[row_index]
                new_row = []
                row = [num for num in current_row.split(" ") if num != ""]
                for column_index in range(len(row)):
                    new_row.append(False)
                    value = row[column_index]
                    self.entries[value] = (row_index, column_index)
                self.rows.append(new_row)

    def __repr__(self) -> str:
        s = [[str(e) for e in row] for row in self.rows]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return '\n'.join(table)

    @property
    def bingo(self) -> bool:
        for row in self.rows:
            if all(row):
                return True
        for column in range(len(self.rows[0])):
            if all([row[column] for row in self.rows]):
                return True

        return False

    def score(self, num: int) -> int:
        unmarked_sum = 0
        for entry in self.entries:
            row, column = self.entries[entry]
            if not self.rows[row][column]:
                unmarked_sum += int(entry)
        return unmarked_sum * int(num)

    def toggle(self, num: str) -> None:
        if num in self.entries:
            row, column = self.entries[num]
            self.rows[row][column] = True


def parse(puzzle_input):
    """Parse input"""
    data = puzzle_input.splitlines()
    bingo_input = data[0].split(',')
    boards = []

    new_board = []
    # Assume the boards start on line 3
    for line in data[2:]:
        if line.strip() == '':
            # new board
            boards.append(BingoBoard(new_board))
            new_board = []
        else:
            new_board.append(line)
    # Don't lose track of the last board
    boards.append(BingoBoard(new_board))

    return bingo_input, boards


def part1(data):
    """Solve part 1"""
    bingo_input, boards = data
    for num in bingo_input:
        for board in boards:
            board.toggle(num)
            if board.bingo:
                return board.score(num)


def part2(data):
    """Solve part 2"""
    bingo_input, boards = data
    for num in bingo_input:
        for board in boards:
            board.toggle(num)
            if len(boards) == 1 and boards[0].bingo:
                return boards[0].score(num)
        boards = [board for board in boards if not board.bingo]
    return 0


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    answer_a, answer_b = solve(puzzle_input=data)
    print(answer_b)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
