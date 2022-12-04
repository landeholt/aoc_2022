from pathlib import Path
import requests
from pprint import pprint
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

RESULT_DIVIDER = "\n---\n"

env = Environment(loader=FileSystemLoader("./templates/"))


def render(template: str, **data):
    return env.get_template(f"{template}.py.j2").render(**data)


def get(day, path: str = ""):
    from aoc_2022.env import cookies, year

    return requests.get(
        f"https://adventofcode.com/{year}/day/{day}{path}", cookies=cookies
    ).text


def post(day, data):
    from aoc_2022.env import cookies, year

    return requests.post(
        f"https://adventofcode.com/{year}/day/{day}/answer", cookies=cookies, data=data
    ).text


def get_remote_input(day: int):
    return get(day, "/input")


def get_remote_data(day: int):
    from bs4 import BeautifulSoup

    html_doc = get(day)
    bs = BeautifulSoup(html_doc, "html.parser")
    try:
        data = [bs.find("pre").find("code").text]  # type: ignore
        answers = [e.text for e in bs.select("code em")[-2:]]
        data += answers
        return RESULT_DIVIDER.join(data)
    except AttributeError:
        return


def parse_result(html_doc):
    from bs4 import BeautifulSoup
    import re

    bs = BeautifulSoup(html_doc, "html.parser")
    try:
        text = bs.find("article").find("p").text  # type: ignore
        match = re.match(r"(That's not the right answer\.|)", text)
        if match:
            return "Incorrect"
        return "Correct"
    except AttributeError:
        return "Retry manually.."


DAY_FOLDER = lambda day: Path(f"aoc_2022/day{day:0>2}")
TEST_DAY_FILE = lambda day: Path(f"tests/test_day{day:0>2}.py")


def present(data):
    pprint(data)


def get_local_input(day: int, data_file="data.txt"):
    import re

    data = re.split(rf"{RESULT_DIVIDER}", (DAY_FOLDER(day) / data_file).read_text())
    if len(data) == 3:
        return data[0], {"first": data[1].strip(), "second": data[2].strip()}
    if len(data) == 2:
        return data[0], {"first": data[1].strip(), "second": None}
    return data[0], {"first": None, "second": None}


def scaffold_day(day: int, data=None):
    folder = DAY_FOLDER(day)
    if not folder.exists():
        folder.mkdir()
        data_file = folder / "data.txt"
        data_file.touch()
        if data:
            data_file.write_text(data=data)
        core = folder / "core.py"
        core.touch()
        core.write_text(data=render("core", day=day))

    test = TEST_DAY_FILE(day)
    if not test.exists():
        test.touch()
        test.write_text(data=render("test", day=day, day_formatted=f"{day:0>2}"))

    return folder


def remove_day(day: int):
    def rm_tree(path):
        path = Path(path)
        for child in path.glob("*"):
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
    return getattr(locals["core"], puzzle)
