import sys
from math import gcd
from itertools import count


def lcm(x, y):
    return x*y // gcd(x, y)


def part2(filename: str):
    with open(filename) as f:
        all_times = f.readline().strip().split(",")
        bus_times = []
        for i, v in filter(lambda i_and_time: i_and_time[1] != 'x', enumerate(all_times)):
            bus_times.append((i, int(v)))

    print(bus_times)

    s_time, advance_by = bus_times[0]
    # all_set = []

    for offset, next_bus in bus_times[1:]:
        # https://docs.python.org/3/library/itertools.html#itertools.count
        for time in count(s_time, advance_by):
            if (time + offset) % next_bus == 0:  # it departs when we want
                # all_set.append(next_bus)
                break
        # if len(all_set) == len(bus_times) - 1:
            # print(f'all set: {all_set}')

            # return all_set
        # else:
            # all_set = []
        # go to next multiple
        advance_by = lcm(advance_by, next_bus)
        s_time = time
        print(f'advance to next: {advance_by}')

    print(time)

    for offset, bus_id in bus_times:
        print(f'{time + offset}:{(time + offset) % bus_id}')


if __name__ == "__main__":
    part2(sys.argv[1])
