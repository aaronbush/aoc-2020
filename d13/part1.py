import sys


def part1(filename: str):
    with open(filename) as f:
        target_time = int(f.readline().strip())
        bus_times = f.readline().strip().split(",")
        bus_times = [int(time) for time in bus_times if not time == 'x']

    bus_deltas = {}

    # hmm
    for bus_id in bus_times:
        n, r = divmod(target_time, bus_id)

        if not r == 0:
            n += 1
        time_delta = n*bus_id - target_time
        bus_deltas[bus_id] = time_delta, time_delta * bus_id

    print(target_time)
    print(bus_times)
    print(bus_deltas)


if __name__ == "__main__":
    part1(sys.argv[1])
