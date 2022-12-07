from collections import defaultdict
from functools import reduce
import re

key = "__dir__"


def cd(state, proc):
    actions = {"..": list.pop, "/": list.clear}
    match = re.match(r"\$ cd (.+)", proc)
    paths = state[key]
    if not match:
        return
    path = match.group(1)
    if path in actions:
        actions[path](paths)
    else:
        paths.append(path)


def size(state, proc):
    match = re.match(r"(\d+) (\S+)", proc)
    if not match:
        return

    size, file = match.groups()
    size = int(size)
    parts = ["."] + state[key] + [file]
    for i, _ in enumerate(parts):
        path = "/".join(parts[:i])
        state[path] += size


def walk(state, proc: str):
    if proc.startswith("$"):
        cd(state, proc)
    else:
        size(state, proc)

    return state


def ls(data: str):
    state = defaultdict(int)
    state[key] = []  # type: ignore
    state = reduce(walk, data.splitlines(), state)
    state.pop("")
    state.pop(key)
    return state


def first(data: str):
    return sum(s for s in ls(data).values() if s <= 100000)


def second(data: str):
    state = ls(data)
    total = 70000000
    space_used = state["."]
    space = 30000000 - (total - space_used)
    return min(state[c] for c in state if state[c] >= space)
