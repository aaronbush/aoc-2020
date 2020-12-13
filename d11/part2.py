import sys
from copy import deepcopy
from typing import Callable, Dict
from dataclasses import dataclass
from os import system


@dataclass
class Coordinate:
    row: int
    col: int
    name: str
    row_op: Callable[[int], int] = lambda n: n
    col_op: Callable[[int], int] = lambda n: n

    def scale(self):
        self.row = self.row_op(self.row)
        self.col = self.col_op(self.col)

    def seat_at(self, seats):
        # print(f'  seat_at: {self.row} / {self.col}')
        return seats[self.row][self.col]


def load_seats(filename: str):
    return [list(line.strip()) for line in open(filename).readlines()]


def print_seats(seats):
    for row in seats:
        print("".join(row))


def num_occupied(seats):
    return sum([r.count('#') for r in seats])


def create_card_and_ords(row, col) -> Dict[str, Coordinate]:
    def dec(n): return n-1
    def inc(n): return n+1
    cards = {}
    cards['n'] = Coordinate(row, col, row_op=dec, name='north')
    cards['s'] = Coordinate(row, col, row_op=inc, name='south')
    cards['e'] = Coordinate(row, col, col_op=inc, name='east')
    cards['w'] = Coordinate(row, col, col_op=dec, name='west')
    cards['ne'] = Coordinate(row, col, row_op=dec,
                             col_op=inc, name='north-east')
    cards['se'] = Coordinate(row, col, row_op=inc,
                             col_op=inc, name='south-east')
    cards['sw'] = Coordinate(row, col, row_op=inc,
                             col_op=dec, name='south-west')
    cards['nw'] = Coordinate(row, col, row_op=dec,
                             col_op=dec, name='north-west')

    for card in cards.values():
        card.scale()
    return cards


def seat_at(row, col, seats):
    return seats[row][col]


def within_bounds(coord: Coordinate, seats) -> bool:
    ok = 0 <= coord.col < len(seats[0]) and 0 <= coord.row < len(seats)
    # print(f'checking ({ok}): {coord}')
    return ok


def new_seat_value(row, col, seats):
    current_seat = seat_at(row, col, seats)

    if current_seat == '.':
        return '.'

    seen_occupied = 0

    cards = create_card_and_ords(row, col)

    while True:
        valid_coords = [(d, card) for d, card in cards.items()
                        if within_bounds(card, seats)]

        # print(f'from({row}/{col}) : seen {seen_occupied} occupied')
        # print(f'{valid_coords}')
        if not valid_coords:
            # done looking - if we are open and didn't see any occupied the sit
            if current_seat == 'L' and seen_occupied == 0:
                return '#'
            return current_seat

        for d, coord in valid_coords:
            if coord.seat_at(seats) == '#' or coord.seat_at(seats) == 'L':
                # stop searching in this direction
                del(cards[d])
                # print(f'removing: {d}')
                if coord.seat_at(seats) == '#':  # occupied
                    seen_occupied += 1

            # currently occupied and 5 of 'adjacent' are also occupied then open it up
            if current_seat == '#' and seen_occupied == 5:
                return 'L'

            if current_seat == 'L' and seen_occupied > 0:
                return 'L'

            coord.scale()


def part2(filename: str):
    seats = load_seats(filename)
    num_rows = len(seats)
    num_cols = len(seats[0])
    current = deepcopy(seats)  # keep load state for show

    i = 0
    while True:
        prev = deepcopy(current)

        for row in range(0, num_rows):
            for col in range(0, num_cols):
                v = new_seat_value(row, col, prev)
                # print(f'{row}/{col}: new seat = {v}')
                current[row][col] = v

        system('clear')
        print_seats(current)

        if prev == current:
            print(f'stable at {i}')
            print(f'occupied: {num_occupied(current)}')
            break
        i += 1


if __name__ == "__main__":
    part2(sys.argv[1])
