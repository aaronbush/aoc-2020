import sys
from itertools import combinations


def part1(filename: str, preamble_len: int) -> int:
    data = [int(line.strip()) for line in open(filename).readlines()]
    i = preamble_len
    for num in data[preamble_len:]:
        found_pair = False
        for s in combinations(data[i-preamble_len:i], 2):
            if sum(s) == num:
                found_pair = True
                break
        if not found_pair:
            return num
        i += 1


def part2a(filename: str, search_for: int):
    data = [int(line.strip()) for line in open(filename).readlines()]
    for i in range(len(data)):
        sum = 0
        for j, num in enumerate(data[i:]):
            sum += num
            if sum == search_for:
                # print(f'bingo {data[i:i+j+1]}')
                return data[i:i+j+1]
            if sum > search_for:
                break  # too far


if __name__ == "__main__":
    p1_res = part1(sys.argv[1], int(sys.argv[2]))
    print(f'part 1: {p1_res} has no pairs')
    assert p1_res == 31161678

    res = part2a(sys.argv[1], p1_res)
    print(f'part 2: min:{min(res)} max:{max(res)}')
    assert min(res) == 1212280
    assert max(res) == 4241588
