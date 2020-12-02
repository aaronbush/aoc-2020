from typing import Iterable, Tuple
from itertools import combinations


def read_input(filename: str) -> [int]:
    with open(filename) as f:
        data = f.readlines()
        data = [int(l) for l in data]
        return data


def find_sum_to(total: int, ints: Iterable[int]) -> Tuple[int]:
    for t in ints:
        if sum(t) == total:
            return t
    raise RuntimeError("oops")


def solve(combo_len: int = 2):
    nums = read_input("d1/d1.input")
    nums = combinations(nums, combo_len)
    result = find_sum_to(2020, nums)
    print(f"found: {result}")
