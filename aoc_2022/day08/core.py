import math
from typing import Generator, List, Tuple

Grid = List[List[int]]


def shape(grid: Grid):
    return len(grid), len(grid[0])


def path(ra: range, fn) -> Generator[Tuple[int, int], None, None]:
    for k in ra:
        r = fn(k)
        if r[0] >= 0 and r[1] >= 0:
            yield r


def ileft(grid: Grid, i, j):
    _, y = shape(grid)
    return filter(lambda p: p != (i, j), path(range(1, y), lambda k: (i, j-k)))


def iright(grid: Grid, i, j):
    _, y = shape(grid)
    return filter(lambda p: p != (i, j), path(range(y-j), lambda k: (i, j+k)))


def iup(grid: Grid, i, j):
    x, _ = shape(grid)
    return filter(lambda p: p != (i, j), path(range(1, x), lambda k: (i-k, j)))


def idown(grid: Grid, i, j):
    x, _ = shape(grid)
    return filter(lambda p: p != (i, j), path(range(x-i), lambda k: (i+k, j)))


def isvisible(grid: Grid, i, j):
    paths = [iup, idown, ileft, iright]

    for path in paths:
        if all(grid[i][j] > grid[pi][pj] for pi, pj in path(grid, i, j)):
            return True
    return False


def isedge(grid: Grid, i, j):
    x, y = shape(grid)
    return x-1 == i or y-1 == j or i == 0 or j == 0


def distance(pi, pj, qi, qj):
    return int(math.sqrt(math.pow((qi - pi), 2) + math.pow((qj - pj), 2)))


def get_scenic_score(grid: Grid, i, j):
    paths = [iup, idown, ileft, iright]
    score = 1
    for path in paths:
        t = 0
        for pi, pj in path(grid, i, j):
            t += 1
            if grid[pi][pj] >= grid[i][j]:
                break
        score *= t
    
    if score == 1:
        return 0
    else:
        return score


def first(data: str):
    grid = [list(map(int, list(d))) for d in data.splitlines()]
    x, y = shape(grid)
    total = 0
    for i in range(1, x-1):
        total += sum(isvisible(grid, i, j) for j in range(1, y-1))
    return x * 2 + (y-2)*2 + total


def second(data: str):
    grid = [list(map(int, list(d))) for d in data.splitlines()]
    x, y = shape(grid)
    scores = []
    for i in range(x):
        for j in range(y):
            scores.append(get_scenic_score(grid, i, j))
    return max(scores)
