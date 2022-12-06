# a packet is indicated by a sequence of 4 chars that are all different

# identify the first position of the 4 most recent received chars were all different

from aoc_2022.utils import isdistinct

def subroutine(stream: str, size: int):
    return min(i+size for i, _ in enumerate(stream) if isdistinct(stream[i:i+size]))


def first(data: str):
    return subroutine(data, size=4)


def second(data: str):
    return subroutine(data, size=14)
