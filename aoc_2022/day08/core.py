from typing import Generator, List, Tuple

Grid = List[List[int]]


def shape(grid: Grid):
    return len(grid), len(grid[0])


def path(ra: range, fn) -> Generator[Tuple[int, int], None, None]:
    yield from (fn(k) for k in ra)


def filter_path(path: Generator[Tuple[int, int], None, None], i, j):
    yield from (p for p in path if p != (i, j) and p[0] >= 0 and p[1] >= 0)


def ileft(grid: Grid, i, j):
    return path(range(1, len(grid[0])), lambda k: (i, j-k))


def iright(grid: Grid, i, j):
    return path(range(len(grid[0])-j), lambda k: (i, j+k))


def iup(grid: Grid, i, j):
    return path(range(1, len(grid)), lambda k: (i-k, j))


def idown(grid: Grid, i, j):
    return path(range(len(grid)-i), lambda k: (i+k, j))


def isvisible(grid: Grid, i, j):
    paths = [iup, idown, ileft, iright]
    return any(all(grid[i][j] > grid[pi][pj] for pi, pj in filter_path(path(grid, i, j), i, j)) for path in paths)


def get_scenic_score(grid: Grid, i, j):
    paths = [iup, idown, ileft, iright]
    score = 1
    for path in paths:
        t = 0
        for pi, pj in filter_path(path(grid, i, j), i, j):
            t += 1
            if grid[pi][pj] >= grid[i][j]:
                break
        score *= t
    return score if score > 1 else 0


def first(data: str):
    grid = [list(map(int, list(d))) for d in data.splitlines()]
    x, y = shape(grid)
    return x * 2 + (y-2) * 2 + sum(isvisible(grid, i, j) for j in range(1, y-1) for i in range(1, x-1))


def second(data: str):
    grid = [list(map(int, list(d))) for d in data.splitlines()]
    x, y = shape(grid)
    return max(get_scenic_score(grid, i, j) for j in range(y) for i in range(x))
