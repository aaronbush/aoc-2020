import sys
from typing import Tuple


def inc(o, v): return o+v
def dec(o, v): return o-v
def nop(o, v): return o


def update_location(location: Tuple[int, int], amount: int, x_fun=nop, y_fun=nop) -> Tuple[int, int]:
    return (x_fun(location[0], amount), y_fun(location[1], amount))


def rotate(cardinal: str, value: int) -> str:
    deg_cards = {0: 'e', 90: 's', 180: 'w', 270: 'n', 360: 'e'}
    key_list = list(deg_cards.keys())
    val_list = list(deg_cards.values())

    n = key_list[val_list.index(cardinal)]
    n += value

    if (n > 360):
        return deg_cards[divmod(n, 360)[1]]
    else:
        return deg_cards[n]


def navigate(location: Tuple[int, int], instructions: [str]) -> Tuple[int, int]:
    cardinal = 'e'

    for ins in instructions:
        move = ins[0]
        value = int(ins[1:])
        print(f'{move} -> {value}')

        if move == 'R':
            cardinal = rotate(cardinal, value)
        elif move == 'L':
            cardinal = rotate(cardinal, 360-value)

        if move == 'E':
            location = update_location(location, value, inc, nop)
        elif move == 'N':
            location = update_location(location, value, nop, inc)
        elif move == 'S':
            location = update_location(location, value, nop, dec)
        elif move == 'W':
            location = update_location(location, value, dec, nop)
        elif move == 'F':
            if cardinal == 'e':
                location = update_location(location, value, inc, nop)
            elif cardinal == 'w':
                location = update_location(location, value, dec, nop)
            elif cardinal == 'n':
                location = update_location(location, value, nop, inc)
            elif cardinal == 's':
                location = update_location(location, value, nop, dec)

        # print(f'{cardinal} {location}')
    return location


def part1(filename: str):
    instructions = [line.strip() for line in open(filename).readlines()]
    # print(instructions)
    location = navigate((0, 0), instructions)
    print(f'distance: {location}: {abs(location[0]) + abs(location[1])}')


if __name__ == "__main__":
    part1(sys.argv[1])
