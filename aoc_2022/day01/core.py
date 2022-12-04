from aoc_2022.toolkit import get_remote_input
from aoc_2022.utils import take

data = get_remote_input(1)


def calorie_generator(data):
    import re

    return (sum(map(int, d.split())) for d in (re.findall(r"((?:\d+\n)+)", data)))


def first(data: str):
    return max(calorie_generator(data))


def second(data: str):
    return sum(take(sorted(calorie_generator(data), reverse=True), n=3))
