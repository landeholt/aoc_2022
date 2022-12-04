from aoc_2022.toolkit import *
from aoc_2022.utils import partition

data = get_remote_input(4)


def parse(data: str):
    import re

    return partition(re.findall(r"(?:(\d+)-(\d+)),?", data), n=2)


def to_range(p):
    return range(int(p[0]), int(p[1]) + 1)


def to_set(pair):
    return (set(to_range(p)) for p in pair)


def contained(pair):
    return int(set.issubset(*to_set(pair)) or set.issuperset(*to_set(pair)))


def intersects(pair):
    return int(not set.isdisjoint(*to_set(pair)))


def first(data: str):
    return sum(map(contained, parse(data)))


def second(data: str):
    return sum(map(intersects, parse(data)))
