import sys
from typing import Tuple, List
from itertools import product


def apply_mask2(bit_pair: Tuple[str, str]) -> str:
    if bit_pair[0] == 'X':
        return 'X'  # stays floating
    elif bit_pair[0] == '0':
        return bit_pair[1]  # existing value
    else:
        return '1'


def get_floating_address(address: str) -> List[int]:
    results = []
    num_x = address.count('X')
    perms = product('01', repeat=num_x)
    for perm in perms:
        result_addr = address
        for i in perm:
            result_addr = result_addr.replace("X", str(i), 1)
        results.append(result_addr)
    return results


def part1(filename: str):
    with open(filename) as f:
        instructions = [line.strip() for line in f.readlines()]

    memory = {}
    for ins in instructions:
        if "mask" in ins:
            txt_mask = ins.split(" ")[2]
        else:
            location = ins.split('[')[1].split(']')[0]
            location_str = format(int(location), '036b')

            value = int(ins.split(" ")[2])
            value_str = format(value, '036b')

            address_mask = "".join([apply_mask2(bit_pair)
                                    for bit_pair in zip(txt_mask, location_str)])

            # print(f'{txt_mask} with {location_str} -> {address_mask}')
            for address in get_floating_address(address_mask):
                address_int = int(address, 2)
                # print(f'{address} ({int(address, 2)})')
                memory[address_int] = (value_str, value)

    print(sum([value[1] for value in memory.values()]))
    # print(memory)


if __name__ == "__main__":
    part1(sys.argv[1])
