from typing import Set, Tuple
from aoc_2022.toolkit import *
from aoc_2022.utils import flat_map, partition

data = get_remote_input(3)


def divide(s: str):
    pivot = len(s) // 2
    return set(s[:pivot]), set(s[pivot:])


def priority(c: str):
    if c.isupper():
        return ord(c) - 38
    return ord(c) - 96


def first(data: str):
    return sum(
        map(
            priority,
            flat_map(lambda s: set.intersection(*s), map(divide, data.splitlines())),
        )
    )


def second(data: str):
    return sum(
        map(
            priority,
            flat_map(
                lambda group: set.intersection(*(set(g) for g in group)),
                partition(data.splitlines(), n=3),
            ),
        )
    )
