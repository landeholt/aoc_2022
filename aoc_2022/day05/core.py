from copy import deepcopy
from typing import Dict, List
from aoc_2022.utils import partition, trans


def parse(data: str):
    import re

    stacks, procedures = data.split("\n\n")
    stacks = stacks.splitlines()
    items = re.findall(r"(\s{3}|\[\w\])[\s\n]?", "".join(stacks[:-1]))
    names = stacks[-1].split()
    procedures = re.findall(r"move (\d+) from (\d+) to (\d+)", procedures)
    return names, items, procedures


def create_stacks(names, items):
    stacks: Dict[str, List[str]] = dict(
        zip(names, trans(partition(items, n=len(names))))
    )
    for k, v in stacks.items():
        stacks[k] = [crate[1] for crate in v if crate.startswith("[")]
    return stacks


def reorder(stacks, procedures, multiple=False):
    for n, f, t in procedures:
        n = int(n)
        crates = deepcopy(stacks[f][:n])
        if not multiple:
            crates.reverse()
        stacks[t] = crates + stacks[t]
        stacks[f] = stacks[f][n:]


def top(stacks):
    return "".join(v[0] for v in stacks.values())


def first(data: str):
    names, items, procedures = parse(data)
    stacks = create_stacks(names, items)
    reorder(stacks, procedures)
    return top(stacks)


def second(data: str):
    names, items, procedures = parse(data)
    stacks = create_stacks(names, items)
    reorder(stacks, procedures, multiple=True)
    return top(stacks)
