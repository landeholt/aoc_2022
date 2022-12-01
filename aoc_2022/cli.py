from typing import cast
import click
import arrow

TABLE = {"1": "first", "2": "second"}


@click.group()
def cli():
    pass


def get_day(day):
    if day == "today":
        return arrow.now().date().day
    if day == "tomorrow":
        return arrow.now().shift(days=1).date().day
    return day

def get_path(path):
    import re
    match = re.match(r"(\d{1,2}|today)?:(1|2)?", path)
    if not match:
        click.echo("Invalid path")
        raise RuntimeError
    
    
    day, puzzle = match.groups()

    if day is None and puzzle is None:
        click.echo("Invalid path")
        raise RuntimeError

    if day is None:
        day = "today"
    if puzzle is None:
        puzzle = "1"

    day = cast(int,get_day(day))
    puzzle = TABLE[puzzle]
    return day, puzzle

@cli.command()
@click.argument('day', default="today")
def create(day):
    """ Setup a single day folder """
    from aoc_2022.toolkit import scaffold_day

    day = get_day(day)
    scaffold_day(day)




@cli.command()
@click.argument('day', default="today")

def remove(day):
    """ Remove a single day folder """
    from aoc_2022.toolkit import remove_day

    day = get_day(day)
    remove_day(day)

@cli.command()
@click.option("-r", "--remote", prompt=True, prompt_required=False, default=True, is_flag=True)
@click.argument("path", default="today:1")
def run(path, remote):
    """ Run a days functions"""
    from aoc_2022.toolkit import get_puzzle_fn, get_local_input, get_remote_input
    prefix = f"[ {'LOCAL' if not remote else 'REMOTE'} ] "
    try:
        day, puzzle = get_path(path)
    except RuntimeError:
        return
    try:
        fn = get_puzzle_fn(day, puzzle)
        click.echo(prefix + f"Running {puzzle} puzzle for {arrow.now().replace(month=12,day=int(day)).format('DD MMMM')}")
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
@click.option("--all", default=False, is_flag=True)
@click.option("--intra", default=False, is_flag=True)
def test(path, intra, all):
    try:
        day, puzzle = get_path(path)
    except RuntimeError:
        return
    
    import pytest
    
    if all:
        pytest.main(["tests/", "-v"])
    elif all and intra:
        pytest.main([f"tests/test_day{day:0>2}.py", "-v"])
    else:
        pytest.main([f"tests/test_day{day:0>2}.py::test_{puzzle}", "-v", "-s"])


if __name__ == "__main__":
    cli()
