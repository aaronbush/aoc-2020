import sys


def midpoint(low: int, high: int) -> int:
    return (high - low) // 2


def seek(low: int, high: int, high_char: chr, instructions: str) -> int:
    for c in instructions:
        if c == high_char:  # keep top 1/2
            low = low+1 + midpoint(low, high)
        else:  # keep bottom 1/2
            high = low + midpoint(low, high)
        # print(f'{c}: from {low} - {high}')
    assert low == high
    return high


def main(filename: str):
    with open(filename) as f:
        for l in f:
            fb_instructions = l[:7]
            lr_instructions = l[7:]
            low = 0
            high = 127
            row = seek(low, high, 'B', fb_instructions)
            # print(f'{low}-{high}: {row}')

            low = 0
            high = 7
            col = seek(low, high, 'R', lr_instructions)
            # print(f'{low}-{high}: {col}')
            print(row*8 + col)


'''
for part 2:
    run this and sort output and save to file
    look at top/bottom of saved output for high/low
    run `seq low high` and save to another file
    diff the two files
'''
if __name__ == "__main__":
    main(sys.argv[1])
