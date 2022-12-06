from aoc_2022.toolkit import get_remote_input
from aoc_2022.utils import take

data = get_remote_input(1)


def elf_finder(data):
    import re

    return (sum(map(int, d.split())) for d in (re.findall(r"((?:\d+\n)+)", data)))


def first(data: str):
    return max(elf_finder(data))


def second(data: str):
    return sum(take(sorted(elf_finder(data), reverse=True), n=3))
