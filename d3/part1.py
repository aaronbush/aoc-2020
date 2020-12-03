import sys
from typing import Tuple


class Forest:
    def __init__(self):
        self._forest = []
        self._width = 0

    def addRow(self, row: str):
        # could try to use 0xblah and then << as we scroll through
        if self._width == 0:
            self._width = len(row.strip()) - 1

        self._forest.append(
            [False if spot == '.' else True for spot in row.strip()])

    @property
    def num_rows(self) -> int:
        return len(self._forest)

    def hit_a_tree(self, row: int, column: int) -> bool:
        i = column % (self._width + 1)
        return self._forest[row][i]

    def __str__(self):
        res = f"width: {self._width} num rows: {self.num_rows}\n"
        for row in self._forest:
            res += str("".join(["#" if s else "." for s in row])) + "\n"
        return res


def read_input(filename: str) -> Forest:
    with open(filename) as f:
        forest = Forest()
        for l in f:
            forest.addRow(l)
    return forest


def solve(forest: Forest, filename: str, slope: Tuple[int] = (3, 1)) -> int:
    col = slope[0]
    hit_count = 0
    for row in range(slope[1], forest.num_rows, slope[1]):
        if forest.hit_a_tree(row, col):
            hit_count += 1
        col += slope[0]
    return hit_count


def main(filename: str):
    forest = read_input(filename)
    # print(forest)
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    res = 1
    for slope in slopes:
        num = solve(forest, filename, slope=slope)
        print(f"{slope} hit {num}")
        res *= num
    print(res)


if __name__ == "__main__":
    main(sys.argv[1])
