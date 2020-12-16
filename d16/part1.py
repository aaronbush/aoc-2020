import sys
from typing import Iterable, List, Tuple
from dataclasses import dataclass


@dataclass
class Rule:
    name: str
    expressions: str
    expression_parsed: List[Tuple[int, int]]

    def __init__(self, name: str, expressions: str):
        self.name = name
        self.expressions = expressions
        self.expression_parsed = []
        for value_range in self.expressions.split('or'):
            min, max = int(value_range.split(
                '-')[0]), int(value_range.split('-')[1])
            self.expression_parsed.append((min, max))

    def is_valid(self, data: int) -> bool:
        results = []
        for condition in self.expression_parsed:
            results.append(condition[0] <= data <= condition[1])
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


def filter_valid_tickets(Rules: Iterable[Rule], nearby_tickets: Iterable[List[int]]):
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


def values_are_valid_for(rules: [Rule], values: [int]) -> [str]:
    possible_field = []
    for rule in rules:
        rule_results = []
        for value in values:
            rule_results.append(rule.is_valid(value))
        if all(rule_results):
            possible_field.append(rule.name)
    return possible_field


def part2(rules: [Rule], nearby_tickets: [[int]], our_ticket: [int]):
    valid_tickets = filter_valid_tickets(rules, nearby_tickets)
    field_col_mapping = {}
    num_fields = len(our_ticket)

    while len(field_col_mapping) < num_fields:
        for i in range(num_fields):
            column_values = [nearby[i] for nearby in valid_tickets]
            column_values.append(our_ticket[i])
            # print(column_values)

            possible_fields = values_are_valid_for(rules, column_values)
            # print(possible_fields)

            # for known mappings remove
            for field in field_col_mapping.keys():
                if field in possible_fields:
                    possible_fields.remove(field)

            if len(possible_fields) == 1:
                field_col_mapping[possible_fields[0]] = i
            else:
                continue
                # was expecting this to be a trick :|
                raise UserWarning(
                    f'({i})dupes: {possible_fields} / {field_col_mapping}')
            # print(possible_fields)

    print(field_col_mapping)
    return field_col_mapping


if __name__ == "__main__":
    rules_filename = sys.argv[1]
    nearby_filename = sys.argv[2]

    rules = list(parse_rules(rules_filename))
    nearby_tickets = list(parse_nearby_tickets(nearby_filename))

    # Part 1
    results = part1(rules, nearby_tickets)
    print(f'p1: {results} -> {sum(results)}')

    # Part 2
    our_ticket = [191, 61, 149, 157, 79, 197, 67, 139, 59,
                  71, 163, 53, 73, 137, 167, 173, 193, 151, 181, 179]
    # our_ticket = [11, 12, 13]
    field_col_mapping = part2(rules, nearby_tickets, our_ticket)
    dep_field = [14, 8, 12, 19, 4, 2]  # just copied from the print out
    p2_result = 1
    for i in dep_field:
        print(our_ticket[i])
        p2_result = p2_result * our_ticket[i]
    print(f'p2: {p2_result}')
