from typing import Set


def is_disjoint(first: Set, second: Set):
    return 0 == len(first.intersection(second))
