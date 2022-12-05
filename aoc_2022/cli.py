from typing import cast
import click
import arrow

from aoc_2022.utils import first

TABLE = {"1": "first", "2": "second"}
REVERSE_TABLE = {"first": "1", "second": "2"}


@click.group()
def cli():
    pass


def get_day(day):
    if day == "today":
        return arrow.now().date().day
    if day == "tomorrow":
        return arrow.now().shift(days=1).date().day
    return day

def get_formatted_day(day):
    return arrow.now().replace(month=12,day=int(day)).format('DD MMMM')

def get_path(path):
    import re

    match = re.match(r"(\d{1,2}|today)?(?:\:(1|2))?", path)
    if not match:
        click.echo("Invalid path")
        raise RuntimeError

    day, puzzle = match.groups()

    if day is None and puzzle is None:
        click.echo("Invalid path")
        raise RuntimeError

    if day is None:
        day = "today"
    return day, puzzle


@cli.command()
@click.argument("day", default="today")
@click.option("-t", "--track", default=True)
def create(day, track):
    """Setup a single day folder"""
    from aoc_2022.toolkit import scaffold_day, get_remote_data, create_stat
    from time import monotonic

    day = get_day(day)
    data, description = get_remote_data(day)
    folder = scaffold_day(day, data, description)
    if data is None:
        click.echo(f"Was not able to scrape puzzle data for day {day:0>2}")
        click.echo("Please fill it in manually before testing.")
    else:
        click.echo(f"Scaffold created at {folder.as_posix()}")
        data_file = first(folder.glob("*.txt"))
        if data_file:
            click.echo(f"Please verify that {data_file.as_posix()} is correct.")
    if track:
        ts = arrow.now()
        create_stat("create", day, int(ts.timestamp()))
        click.echo(f"A timer was started at {ts.format('HH:mm:ss')}. Good luck!")


@cli.command()
@click.argument("day", default="today")
def remove(day):
    """Remove a single day folder"""
    from aoc_2022.toolkit import remove_day

    day = get_day(day)
    remove_day(day)


@cli.command()
@click.option(
    "-r", "--remote", prompt=True, prompt_required=False, default=True, is_flag=True
)
@click.argument("path", default="today:1")
def run(path, remote):
    """Run a days functions"""
    from aoc_2022.toolkit import get_puzzle_fn, get_local_input, get_remote_input

    prefix = f"[ {'LOCAL' if not remote else 'REMOTE'} ] "
    try:
        day, puzzle = get_path(path)
        day = cast(int,get_day(day))
        puzzle = TABLE[puzzle]
    except RuntimeError:
        return
    try:
        fn = get_puzzle_fn(day, puzzle)
        click.echo(
            prefix
            + f"Running {puzzle} puzzle for {get_formatted_day(day)}"
        )
        if not remote:
            click.echo(fn(get_local_input(day)))
        else:
            click.echo(fn(get_remote_input(day)))

    except KeyError as e:
        click.echo(prefix + f"Cannot find puzzle for: {e}")
    except ModuleNotFoundError as e:
        click.echo(prefix + f" Puzzle day{day:0>2}:{puzzle} doesnt exist")


@cli.command()
@click.argument("path", default="today:1")
def submit(path):
    """Submit a puzzle"""
    from aoc_2022.toolkit import (
        get_puzzle_fn,
        get_remote_input,
        post,
        create_stat,
        check_stat,
    )

    try:
        day, puzzle = get_path(path)
        day = cast(int,get_day(day))
        puzzle = TABLE[puzzle]
    except RuntimeError:
        return
    try:
        fn = get_puzzle_fn(day, puzzle)
        click.echo(
            f"Running {puzzle} puzzle for {arrow.now().replace(month=12,day=int(day)).format('DD MMMM')}"
        )
        answer = fn(get_remote_input(day))
        ts = arrow.now()
        click.echo(f"submitting: {answer}")
        result = post(day, {"level": REVERSE_TABLE[puzzle], "answer": answer})
        passed = "That's the right answer" in result
        create_stat(
            "submit",
            day,
            int(ts.timestamp()),
            part=puzzle,
            answer="pass" if passed else "fail",
        )

        if passed:
            click.echo("Answer accepted, good job!")
            time_spent = check_stat("submit", day, puzzle)
            if time_spent:
                click.echo(f"{puzzle} part took {time_spent} to pass.")
            return

        click.echo("Wrong answer..")

    except KeyError as e:
        click.echo(f"Cannot find puzzle for: {e}")
    except ModuleNotFoundError as e:
        click.echo(f" Puzzle day{day:0>2}:{puzzle} doesnt exist")


@cli.command()
@click.argument("path", default="today:1")
def test(path):
    from aoc_2022.toolkit import create_stat, check_stat
    import pytest

    try:
        day, puzzle = get_path(path)
        puzzle = TABLE[puzzle]
    except RuntimeError:
        return

    result = pytest.main([f"tests/test_day{day:0>2}.py::test_{puzzle}", "-v", "-s"])

    ts = arrow.now()
    create_stat(
        "test",
        day,
        int(ts.timestamp()),
        part=puzzle,
        answer="pass" if result != 1 else "fail",
    )

    time_spent = check_stat("test", day, puzzle)
    if time_spent:
        click.echo(f"{puzzle} part took {time_spent} to pass.")

@cli.command()
@click.argument("path", default="today")
def stats(path):
    from aoc_2022.toolkit import check_stat

    def message(day, puzzle):
        test_ts = check_stat('test', day, puzzle)
        if test_ts:
            click.echo(f"[Testing] {puzzle.capitalize()} passed {test_ts}")
        submit_ts = check_stat('submit', day, puzzle)
        if submit_ts:
            click.echo(f"[Submission] {puzzle.capitalize()} passed {submit_ts}")
    try:
        day, puzzle = get_path(path)
        day = cast(int,get_day(day))

    except RuntimeError:
        return
    click.echo(f"Stats for {get_formatted_day(day)}:\n")
    if puzzle:
        puzzle = TABLE[puzzle]
        message(day, puzzle)
    else:
        message(day, 'first')
        message(day, 'second')
    
        


if __name__ == "__main__":
    cli()
