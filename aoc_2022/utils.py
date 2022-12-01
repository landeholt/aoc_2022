from typing import Generator, Iterable, TypeVar

T = TypeVar("T")

def take(data: Iterable[T], n: int = 1) -> Generator[T, None, None]:
    for i, d in enumerate(data, 1):
        yield d
        if i == n:
            break

def intmap(data: Iterable[str]):
    return map(int, data)
