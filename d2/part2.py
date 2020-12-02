from typing import Iterable
from dataclasses import dataclass

input_file = "d2/p1.input"


@dataclass
class PasswordRule:
    rule_range: str
    rule_value: str
    example_value: str

    def check(self) -> bool:
        min, max = self.rule_range.split("-")
        return self.example_value.count(self.rule_value) in range(int(min), int(max)+1)

    def check2(self) -> bool:
        i, j = self.rule_range.split("-")
        i = int(i) - 1
        j = int(j) - 1
        combined = self.example_value[i]+self.example_value[j]
        return combined.count(self.rule_value) == 1


def get_rules(filename: str) -> Iterable[PasswordRule]:
    with open(filename) as f:
        for l in f:
            rule, example = l.split(":")
            rule_range, rule_value = rule.split()
            yield PasswordRule(rule_range, rule_value, example.strip())


def check_rules():
    num_ok = 0
    for rule in get_rules(input_file):
        if rule.check2():
            # print(rule)
            num_ok += 1

    print(f"Number of pass: {num_ok}")
