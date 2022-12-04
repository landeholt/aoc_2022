from itertools import chain, islice
from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


def take(data: Iterable[T], n: int = 1) -> Generator[T, None, None]:
    for i, d in enumerate(data, 1):
        yield d
        if i == n:
            break


def first(data: Iterable[T], default = None):
    try:
        result, *_ = take(data, n=1)
        return result
    except ValueError:
        return default


def flat_map(fn, seq: Iterable[Iterable[T]]) -> Generator[T, None, None]:
    return (y for ys in seq for y in fn(ys))


def partition(seq: Iterable[T], n=1) -> "Generator[chain[T], None, None]":
    iterator = iter(seq)
    for first in iterator:
        yield chain([first], islice(iterator, n - 1))


def intmap(data: Iterable[str]):
    return map(int, data)


def trans(data: Iterable[Iterable[T]]) -> Iterable[Iterable[T]]:
    return map(list, zip(*data))


def str_trans(data: Iterable[Iterable[T]]):
    def join(x):
        return "".join(x)

    return map(join, zip(*data))


def argmin(a):
    return min(range(len(a)), key=lambda x: a[x])


def argmax(a):
    return max(range(len(a)), key=lambda x: a[x])
