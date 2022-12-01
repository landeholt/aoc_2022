from pathlib import Path
from typing import Iterable, TypeVar
import requests
from pprint import pprint
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

RESULT_DIVIDER = r"\n---\n"

env = Environment(loader=FileSystemLoader("./templates/"))

def render(template: str, **data):
    return env.get_template(f"{template}.py.j2").render(**data)

def get_remote_input(day: int):
    from aoc_2022.env import cookies
    return requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies).text

DAY_FOLDER = lambda day : Path(f"aoc_2022/day{day:0>2}")
TEST_DAY_FILE = lambda day : Path(f"tests/test_day{day:0>2}.py")
def present(data):
    pprint(data)

T = TypeVar("T")

def take(data: Iterable[T], n: int = 1):
    for i, d in enumerate(data, 1):
        yield d
        if i == n:
            break

def get_local_input(day: int):
    import re
    return re.split(RESULT_DIVIDER,(DAY_FOLDER(day) / "data.txt").read_text())


def scaffold_day(day: int):        
    folder = DAY_FOLDER(day)
    if not folder.exists():
        folder.mkdir()
        (folder / "data.txt").touch()
        core = folder / "core.py"
        core.touch()
        core.write_text(data=render("core", day=day))


    test = TEST_DAY_FILE(day)
    if not test.exists():
        test.touch()
        test.write_text(data=render("test", day=day, day_formatted=f"{day:0>2}"))

def remove_day(day: int):
    def rm_tree(path):
        path = Path(path)
        for child in path.glob('*'):
            if child.is_file():
                child.unlink()
            else:
                rm_tree(child)
        path.rmdir()

    folder = DAY_FOLDER(day)
    if folder.exists():

        rm_tree(folder)
    
    test = TEST_DAY_FILE(day)
    if test.exists():
        test.unlink()


def get_puzzle_fn(day: int, puzzle: str):
    locals = {}
    exec(f"from aoc_2022.day{day:0>2} import core", None, locals)
    return getattr(locals['core'], puzzle)
