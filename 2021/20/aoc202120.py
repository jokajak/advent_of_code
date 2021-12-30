"""AoC 20, 2021.

The image enhancement algorithm describes how to enhance an image by simultaneously converting all pixels in the input
image into an output image. Each pixel of the output image is determined by looking at a 3x3 square of pixels centered
on the corresponding input image pixel. So, to determine the value of the pixel at (5,10) in the output image, nine
pixels from the input image need to be considered: (4,9), (4,10), (4,11), (5,9), (5,10), (5,11), (6,9), (6,10), and
(6,11). These nine input pixels are combined into a single binary number that is used as an index in the image
enhancement algorithm string.

For example, to determine the output pixel that corresponds to the very middle pixel of the input image, the nine pixels
marked by [...] would need to be considered:

# . . # .
#[. . .].
#[# . .]#
.[. # .].
. . # # #

Starting from the top-left and reading across each row, these pixels are ..., then #.., then .#.; combining these forms
...#...#.. By turning dark pixels (.) into 0 and light pixels (#) into 1, the binary number 000100010 can be formed,
which is 34 in decimal.
"""

# Standard library imports
import pathlib
import sys
from collections import defaultdict
from aocd import data as input_data, submit


class TrenchMap:
    def __init__(self, algorithm: list, input_image: defaultdict) -> None:
        self.algorithm = algorithm
        self.image = input_image
        min_x = min_y = sys.maxsize
        max_x = max_y = 0
        for coords in input_image.keys():
            if coords == "infinity":
                continue
            x, y = coords
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def get_output_pixel_index(self, x, y) -> int:
        """Calculate input pixel string.

        Starting from the top-left and reading across each row, these pixels are ..., then #.., then .#.; combining
        these forms ...#...#.. By turning dark pixels (.) into 0 and light pixels (#) into 1, the binary number
        000100010 can be formed, which is 34 in decimal.

        The image enhancement algorithm string is exactly 512 characters long, enough to match every possible 9-bit
        binary number. The first few characters of the string (numbered starting from zero) are as follows:
        """
        # fmt: off
        delta_coords = (
            (-1, -1), (-1,  0), (-1,  1),
            ( 0, -1), ( 0,  0), ( 0,  1),  # noqa
            ( 1, -1), ( 1,  0), ( 1,  1),  # noqa
        )
        # fmt: on
        bin_repr = []
        for delta_coord in delta_coords:
            delta_x, delta_y = delta_coord
            bin_repr.append(str(self.image[(x + delta_x, y + delta_y)]))
        bin_repr = int("".join(bin_repr), 2)
        return bin_repr

    def get_output_pixel(self, x, y) -> int:
        """Calculate the output pixel value."""
        pixel_index = self.get_output_pixel_index(x, y)
        return self.algorithm[pixel_index]

    def __str__(self) -> str:
        ret = []
        for x in range(self.min_x - 2, self.max_x + 3):
            row = [
                "#" if self.image[(x, y)] == 1 else "."
                for y in range(self.min_y - 2, self.max_y + 3)
            ]
            ret.append("".join(row))
        return "\n".join(ret)

    @property
    def lit(self) -> int:
        return len([True for k, v in self.image.items() if v == 1])


def image_str_to_dict(input_image: str) -> defaultdict:
    new_grid = defaultdict(int)
    for x, row in enumerate(input_image):
        for y, col in enumerate(row):
            if col == "#":
                new_grid[(x, y)] = 1
            elif col == ".":
                continue
            else:
                raise ValueError
    return new_grid


def enhance(trench_map):
    infinity_val = trench_map.image["infinity"]
    infinity_index = int(str(infinity_val) * 9, 2)
    default_val = trench_map.algorithm[infinity_index]
    new_grid = defaultdict(lambda: default_val)
    for x in range(trench_map.min_x - 1, trench_map.max_x + 2):
        for y in range(trench_map.min_y - 1, trench_map.max_y + 2):
            new_val = trench_map.get_output_pixel(x, y)
            new_grid[(x, y)] = new_val
    return TrenchMap(trench_map.algorithm, new_grid)


def parse(puzzle_input):
    """Parse input.

    The first section is the image enhancement algorithm. It is normally given on a single line, but it has been wrapped
    to multiple lines in this example for legibility. The second section is the input image, a two-dimensional grid of
    light pixels (#) and dark pixels (.).
    """
    image_enhancement_algorithm = puzzle_input.splitlines()[0]
    algorithm = [1 if v == "#" else 0 for v in image_enhancement_algorithm]
    input_image = image_str_to_dict(puzzle_input.splitlines()[2:])
    return algorithm, input_image


def part1(data):
    """Solve part 1.

    Start with the original input image and apply the image enhancement algorithm twice, being careful to account for
    the infinite size of the images. How many pixels are lit in the resulting image?
    """
    algorithm = data[0]
    trench_map = TrenchMap(algorithm, input_image=data[1])
    for _ in range(2):
        trench_map = enhance(trench_map)
        print(trench_map)
    print(trench_map.lit)
    return trench_map.lit


def part2(data):
    """Solve part 2"""
    algorithm = data[0]
    trench_map = TrenchMap(algorithm, input_image=data[1])
    for _ in range(50):
        trench_map = enhance(trench_map)
        #print(trench_map)
    print(trench_map.lit)
    return trench_map.lit


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))

    answer_a, answer_b = solve(puzzle_input=input_data)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
