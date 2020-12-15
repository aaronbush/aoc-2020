import sys


def update_play(nums_spoken, play_num, turn_num):
    n_x = nums_spoken[play_num][1]
    nums_spoken[play_num] = n_x, turn_num
    return nums_spoken


def part1(filename: str):
    with open(filename) as f:
        stop_at = int(f.readline().strip())
        start_with = [int(num) for num in f.readline().strip().split(',')]
    nums_spoken = {}

    for i, num in enumerate(start_with):
        nums_spoken[num] = (i+1, i+1)
        last_num_spoken = num

    print(
        f'playing for {stop_at} spoken numbers, starting with {start_with}/{nums_spoken}')

    for turn_number in range(len(nums_spoken)+1, stop_at+1):
        # try to optimize this to avoid looking back at what we know
        seen_when = nums_spoken[last_num_spoken]
        was_looking_for = last_num_spoken
        last_num_spoken = seen_when[1] - seen_when[0]  # deltas
        if last_num_spoken in nums_spoken:
            update_play(nums_spoken, last_num_spoken, turn_number)
        else:
            nums_spoken[last_num_spoken] = (turn_number, turn_number)

        if turn_number % 1000000 == 0:
            print(
                f'   play # {turn_number} looking for {was_looking_for} resulted in {last_num_spoken}')

    print(
        f'   play # {turn_number} looking for {was_looking_for} resulted in {last_num_spoken}')

    # print(f'plays so far: {nums_spoken}')


if __name__ == "__main__":
    part1(sys.argv[1])
