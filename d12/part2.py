import sys
from typing import Tuple


def inc(o, v): return o+v
def dec(o, v): return o-v
def nop(o, v): return o


def update_location(location: Tuple[int, int], amount: int, x_fun=nop, y_fun=nop) -> Tuple[int, int]:
    new_point = (x_fun(location[0], amount), y_fun(location[1], amount))
    if len(location) > 2:
        return new_point + location[2:]
    return new_point


def rotate_waypoint2(location: Tuple[int, int], waypoint: Tuple[int, int], direction: str, degrees: int) -> Tuple[int, int]:
    for i in range(divmod(degrees, 90)[0]):
        waypoint_offset_x = waypoint[0] - location[0]
        waypoint_offset_y = waypoint[1] - location[1]

        if direction == 'L':
            new_x = location[0] - waypoint_offset_y
            new_y = location[1] + waypoint_offset_x
        else:  # rotate R
            new_x = location[0] + waypoint_offset_y
            new_y = location[1] - waypoint_offset_x

        waypoint = new_x, new_y

    return waypoint


def navigate(location: Tuple[int, int], instructions: [str]) -> Tuple[int, int]:
    waypoint = 10, 1

    for ins in instructions:
        move = ins[0]
        value = int(ins[1:])
        print(f'starting @ waypoint: {waypoint} location:{location}')
        print(f'{move} -> {value}')

        if move == 'R':
            waypoint = rotate_waypoint2(location, waypoint, 'R', value)
        elif move == 'L':
            waypoint = rotate_waypoint2(location, waypoint, 'L', value)

        elif move == 'E':
            waypoint = update_location(waypoint, value, inc, nop)
        elif move == 'W':
            waypoint = update_location(waypoint, value, dec, nop)

        elif move == 'N':
            waypoint = update_location(waypoint, value, nop, inc)
        elif move == 'S':
            waypoint = update_location(waypoint, value, nop, dec)

        elif move == 'F':
            waypoint_offset_x = waypoint[0] - location[0]
            waypoint_offset_y = waypoint[1] - location[1]
            print(
                f'  waypoint offset: ({waypoint_offset_x},{waypoint_offset_y})')

            if waypoint_offset_x < 0:  # nav WEST to waypoint
                new_ship_x = location[0] - abs(waypoint_offset_x*value)
                waypoint_offset_x = new_ship_x - abs(waypoint_offset_x)
            else:  # nav EAST
                new_ship_x = location[0] + waypoint_offset_x*value
                waypoint_offset_x = new_ship_x + waypoint_offset_x

            if waypoint_offset_y < 0:  # nav SOUTH to waypoint
                new_ship_y = location[1] - abs(waypoint_offset_y*value)
                waypoint_offset_y = new_ship_y - abs(waypoint_offset_y)
            else:  # nav NORTH
                new_ship_y = location[1] + waypoint_offset_y*value
                waypoint_offset_y = new_ship_y + waypoint_offset_y

            location = new_ship_x, new_ship_y
            waypoint = waypoint_offset_x, waypoint_offset_y

        print(f'ending @ waypoint: {waypoint} location:{location}\n')

    return location


def part1(filename: str):
    instructions = [line.strip() for line in open(filename).readlines()]
    location = navigate((0, 0), instructions)
    print(f'distance: {location}: {abs(location[0]) + abs(location[1])}')


if __name__ == "__main__":
    part1(sys.argv[1])
