from typing import Iterable
import sys

all_fields = {'cid', 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
ok_missing = {'cid'}


def passports(filename: str) -> Iterable[dict]:
    with open(filename) as f:
        passport_info = {}
        for l in f:
            parts = l.strip().split()
            if len(parts) == 0:
                yield passport_info
                passport_info = {}
                continue
            parts = [part.split(':') for part in parts]
            passport_info = {
                **passport_info, **{parts[i][0]: parts[i][1] for i in range(0, len(parts))}}
        if passport_info != {}:  # cover the case where no newline after last record
            yield passport_info


def main(filename: str):
    valid = 0
    for p in passports(filename):
        if all_fields - set(p.keys()) == ok_missing or all_fields - set(p.keys()) == set():
            valid += 1

    print(valid)


if __name__ == "__main__":
    main(sys.argv[1])
