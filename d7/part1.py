from dataclasses import dataclass
from typing import Set, Iterable, List, Tuple
import sys


@dataclass(eq=True, frozen=True)
class Bag:
    count: int
    color: str
    inner_bags: set = None


def we_hold_bags(s: str) -> bool:
    # sentinel for holds no bags
    return 'no other' not in s


def parse_input(filename: str) -> Iterable[Bag]:
    with open(filename) as f:
        for l in f:
            # chop off first 2 words for 'outer/enclosing' bag
            outer_bag = " ".join(l.split()[:2])

            # split enclosed bags list on comma
            inner_bags = " ".join(l.split()[4:]).split(',')
            enclosed = None

            if we_hold_bags(inner_bags[0]):
                enclosed = set()
                for bag in inner_bags:
                    qty = bag.split()[0]
                    color = " ".join(bag.split()[1:3])
                    enclosed.add(Bag(int(qty), color))

            b = Bag(1, outer_bag, enclosed)
            yield(b)


def bags_that_hold(my_bag_color: str, bags: List[Bag]) -> Iterable[Tuple[Bag, Bag]]:
    for bag in bags:
        if not bag.inner_bags:
            continue
        for inner_bag in bag.inner_bags:
            if inner_bag.color == my_bag_color:
                yield (bag, inner_bag)


def collect_bags_that_hold(color: str, bags: List[Bag], known_bags: Set[str]):
    for bag, _ in bags_that_hold(color, bags):
        if bag.color not in known_bags:
            known_bags.add(bag.color)
            collect_bags_that_hold(bag.color, bags, known_bags)


def what_we_hold(color: str, bags: List[Bag], collection_of_bags: [Bag], scale: int):
    for bag in bags:
        if bag.color == color and bag.inner_bags is not None:
            for inner_bag in bag.inner_bags:
                collection_of_bags.append((inner_bag.count*scale, inner_bag))
                # print(f'{len(collection_of_bags)}: {color} we hold {inner_bag}')
                what_we_hold(inner_bag.color, bags,
                             collection_of_bags, inner_bag.count*scale)
    return collection_of_bags


def main(filename: str):
    search_for = 'shiny gold'
    bag_list = list([bag for bag in parse_input(filename)])

    # Part 1: How many bag colors can eventually contain at least one X color bag?
    where_we_can_go = set()
    collect_bags_that_hold(search_for, bag_list, where_we_can_go)
    assert len(where_we_can_go) == 378
    print(f'{len(where_we_can_go)} bags can hold at least one {search_for}')

    # Part 2
    collection_of_bags = []
    what_we_hold(search_for, bag_list, collection_of_bags, 1)
    total = sum([bag_count for bag_count, _ in collection_of_bags])
    assert total == 27526
    print(f'we will need {total} bags to hold our {search_for} bag')


if __name__ == "__main__":
    main(sys.argv[1])
