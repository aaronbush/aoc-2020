import sys

sum = 0
for l in sys.stdin:
    s = "".join(set(sorted(l.strip())))
    print(f'{s} {len(s)}')
    sum += len(s)

print(sum)
