import sys
from functools import partial
from typing import Tuple, Iterable, Callable, List, Set, Dict
MAX_ADPATER_JUMP = 3

DONE = False


def pairwise_deltas(nums: [int]) -> Iterable[int]:
    for i, num in enumerate(nums):
        if i+1 == len(nums):
            return
        yield nums[i+1] - num


def possible_next(source_level: int) -> Iterable[int]:
    # return range(source_level+1, source_level+MAX_ADPATER_JUMP+1)
    return [source_level+1, source_level+MAX_ADPATER_JUMP]


def solve_rec(current_level: int, available_adapters: [int], adapter_chain: [int],
              term_when: Callable[[int, List[int]], bool], pad: str = "."):
    global DONE
    if term_when(current_level, available_adapters):
        print('done')
        DONE = True
        return
    # print(
    #     f'starting at {current_level} with {available_adapters} / chain is: {adapter_chain}')
    options = [n for n in possible_next(
        current_level) if n in available_adapters]

    for p in options:
        if not DONE:
            # print(f'{pad} try: {p}')
            adapters_left = available_adapters.copy()
            adapters_left.remove(p)
            adapter_chain.append(p)
            solve_rec(p, adapters_left, adapter_chain, term_when, pad + ".")


def solve_rec2(current_level: int, available_adapters: [int], adapter_chain: [int],
               term_when: Callable[[int, List[int]], bool], solutions: [Set[int]], pad: str = "."):
    global DONE
    if term_when(current_level, available_adapters):
        # print('done')
        if adapter_chain not in solutions:
            print(f'added another {len(solutions)}')
            solutions.append(adapter_chain)
        return
    # print(
        # f'starting at {current_level} with {available_adapters} / chain is: {adapter_chain}')
    options = [n for n in possible_next(
        current_level) if n in available_adapters]

    for p in options:
        # print(f'{pad} try: {p}')
        adapters_left = available_adapters.copy()
        current_chain = adapter_chain.copy()
        adapters_left.remove(p)
        current_chain.append(p)
        solve_rec2(p, adapters_left, current_chain,
                   term_when, solutions, pad + ".")


def term_when_none_left(_: int, available_adapters: [int]) -> bool:
    return not available_adapters


def term_when_delta_3(final_level: int, current_level: int, _) -> bool:
    return current_level + 3 >= final_level


def part1(filename: str) -> List[int]:
    adapters = [int(line.strip())
                for line in open(filename).readlines()]
    adapters.sort()
    current_level = 0

    adapter_chain = [0]
    solve_rec(current_level, adapters, adapter_chain, term_when_none_left)
    adapter_chain.append(adapter_chain[-1] + 3)
    print(adapter_chain)
    deltas = list(pairwise_deltas(adapter_chain))
    return deltas

# this does not complete... too much :(


def part2(filename: str) -> Tuple[int, int]:
    adapters = [int(line.strip())
                for line in open(filename).readlines()]
    adapters.sort()
    current_level = 0
    solutions = []
    term = partial(term_when_delta_3, adapters[-1]+3)
    adapter_chain = [0]

    solve_rec2(current_level, adapters, adapter_chain, term, solutions)


def part2_3(filename: str):
    deltas = part1(filename)

    nums = []
    in_grp = False
    grp_count = 0

    for delta in deltas:
        if delta == 1:
            in_grp = True
            grp_count += 1
        else:
            in_grp = False
            if grp_count > 0:
                nums.append(grp_count)
            grp_count = 0

    product = 1
    for n in nums:
        if n == 2:
            product *= 2
        elif n == 3:
            product *= 4
        elif n == 4:
            product *= 7
    print(nums)
    print(product)


if __name__ == "__main__":
    # deltas = part1(sys.argv[1])
    # ones, threes = (deltas.count(1), deltas.count(3))
    # print(f'ones: {ones}  threes: {threes}')

    # nope - don't do this
    # ones, threes = part2(sys.argv[1])

    part2_3(sys.argv[1])
