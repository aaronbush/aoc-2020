import sys
from typing import Iterable, List
from dataclasses import dataclass


@dataclass
class Rule:
    name: str
    expressions: str

    def is_valid(self, data: int) -> bool:
        results = []
        for value_range in self.expressions.split('or'):
            min, max = int(value_range.split(
                '-')[0]), int(value_range.split('-')[1])  # todo: could save this
            results.append(min <= data <= max)

        return any(results)


def parse_rules(filename: str) -> Iterable[Rule]:
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                break
            parts = line.split(':')
            yield Rule(name=parts[0], expressions=parts[1].strip())


def parse_nearby_tickets(filename: str) -> Iterable[List[int]]:
    with open(filename) as f:
        for l in f:
            yield list(int(num) for num in l.split(','))


def part1(rules: Iterable[Rule], nearby_tickets: Iterable[List[int]]) -> List[int]:
    invalid_values = []
    for nearby_ticket in nearby_tickets:
        for value in nearby_ticket:
            # print('checking ticket: ', nearby_ticket)
            rule_results = []
            for rule in rules:
                rule_passed = rule.is_valid(value)
                # print(f'{rule.name}/{rule.expressions}:  check({value}) -> {rule_passed}')
                rule_results.append(rule_passed)
            if not any(rule_results):
                invalid_values.append(value)
    return invalid_values


def part2(rules: Iterable[Rule], nearby_tickets: Iterable[List[int]]) -> List[int]:
    valid_tickets = []
    for nearby_ticket in nearby_tickets:
        invalid_values = []
        for value in nearby_ticket:
            rule_results = []
            for rule in rules:
                rule_passed = rule.is_valid(value)
                rule_results.append(rule_passed)
            if not any(rule_results):
                invalid_values.append(value)
                break
        if len(invalid_values) == 0:
            valid_tickets.append(nearby_ticket)
    return valid_tickets


if __name__ == "__main__":
    rules_filename = sys.argv[1]
    nearby_filename = sys.argv[2]

    rules = list(parse_rules(rules_filename))
    nearby_tickets = list(parse_nearby_tickets(nearby_filename))

    # results = part1(rules, nearby_tickets)
    # print(results)
    # print(sum(results))

    valid_tickets = part2(rules, nearby_tickets)
    print(len(valid_tickets))
    print(valid_tickets)
