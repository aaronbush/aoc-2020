import sys
from copy import deepcopy


def load_seats(filename: str):
    return [list(line.strip()) for line in open(filename).readlines()]


def print_seats(seats):
    for row in seats:
        print("".join(row))


def num_occupied(seats):
    return sum([r.count('#') for r in seats])


def copy_seats(seats):
    new_copy = [[None for row in range(len(seats[0]))]
                for col in range(len(seats))]
    for i, row in enumerate(seats):
        for j, col in enumerate(row):
            new_copy[i][j] = col
    return new_copy


def adjacent_coord_pairs(row, col):
    return [
        # (row, col)
        (row-1, col),  # N
        (row-1, col+1),  # NE
        (row, col+1),  # E
        (row+1, col+1),  # SE
        (row+1, col),  # S
        (row+1, col-1),  # SW
        (row, col-1),  # W
        (row-1, col-1)  # NW
    ]


def seat_at(row, col, seats):
    return seats[row][col]


def new_seat_value(row, col, seats):
    # print(f'checking: {seat_at(row, col, seats)}')

    if seat_at(row, col, seats) == '.':
        return '.'

    valid_coords = [(row, col) for row, col in adjacent_coord_pairs(row, col)
                    if 0 <= col < len(seats[0]) and 0 <= row < len(seats)]

    adjacent_seats = [seats[row][col] for row, col in valid_coords]

    if seat_at(row, col, seats) == 'L':  # empty
        if '#' not in set(adjacent_seats):
            return '#'
    else:  # occupied '#'
        if adjacent_seats.count('#') >= 4:
            return 'L'

    return seat_at(row, col, seats)


def part1(filename: str):
    seats = load_seats(filename)
    num_rows = len(seats)
    num_cols = len(seats[0])
    current = deepcopy(seats)  # keep load state for show

    i = 0
    while True:
        # prev = deepcopy(current)
        prev = copy_seats(current)
        # print('prev--------------')
        # print_seats(prev)

        for row in range(0, num_rows):
            for col in range(0, num_cols):
                v = new_seat_value(row, col, prev)
                # print(f'new seat = {v}')
                current[row][col] = v
                # current[row] = current[row][:col] + v + current[row][col+1:]

        # print(f'{i} curr--------------')
        # print_seats(current)

        if prev == current:
            print(f'stable at {i}')
            print(f'occupied: {num_occupied(current)}')
            break
        i += 1


if __name__ == "__main__":
    part1(sys.argv[1])
