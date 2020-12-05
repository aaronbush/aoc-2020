from typing import Iterable
import sys
import re


# mixing this up with regex's so i can learn Python not just re's :)
def cid_re(data: str) -> bool:
    return True


def byr_re(data: str) -> bool:
    try:
        v = int(data)
        return 2002 >= int(v) >= 1920
    except:
        return False


def iyr_re(data: str) -> bool:
    try:
        v = int(data)
        return 2020 >= int(v) >= 2010
    except:
        return False


def eyr_re(data: str) -> bool:
    try:
        v = int(data)
        return 2030 >= int(v) >= 2020
    except:
        return False


def hgt_re(data: str) -> bool:
    m = re.match(r'^([0-9]+)cm$', data)
    if m:
        return 193 >= int(m.group(1)) >= 150
    m = re.match(r'^([0-9]+)in$', data)
    if m:
        return 76 >= int(m.group(1)) >= 59
    return False


def hcl_re(data: str) -> bool:
    m = re.match(r'^#([0-9a-f]{6}$)', data)
    return m != None


def ecl_re(data: str) -> bool:
    valid_colors = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
    return data in valid_colors


def pid_re(data: str) -> bool:
    m = re.match(r'^[0-9]{9}$', data)
    return m != None


all_fields = {'cid', 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
all_fields_patterns = {'cid': cid_re, 'byr': byr_re, 'iyr': iyr_re,
                       'eyr': eyr_re, 'hgt': hgt_re, 'hcl': hcl_re, 'ecl': ecl_re, 'pid': pid_re}
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


def part1(filename: str) -> int:
    valid = 0
    for p in passports(filename):
        if all_fields - set(p.keys()) == ok_missing or all_fields - set(p.keys()) == set():
            valid += 1

    return valid


def part2(filename: str) -> int:  # just run through them a second time - wasteful but ok
    valid = 0
    for p in passports(filename):
        # to check for empty set had to use set()
        if (all_fields - set(p.keys()) == ok_missing
                or all_fields - set(p.keys()) == set()):
            if all([all_fields_patterns[field](value) for field, value in p.items()]):
                valid += 1
    return valid


def part2_test_patterns():
    for field, validator in all_fields_patterns.items():
        try:
            for pass_value in open(f'tests/{field}.test-pass.input').readlines():
                assert validator(pass_value) == True
            for fail_value in open(f'tests/{field}.test-fail.input').readlines():
                assert validator(fail_value) == False
        except FileNotFoundError as fne:
            print(fne)
            continue


if __name__ == "__main__":
    part2_test_patterns()
    print(f'part 1 valid is: {part1(sys.argv[1])}')
    print(f'part 2 valid is: {part2(sys.argv[1])}')
