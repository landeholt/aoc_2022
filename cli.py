from typing import cast
import click
import arrow


@click.group()
def cli():
    pass


def get_day(day):
    if day == "today":
        return arrow.now().date().day
    return day

@cli.command()
@click.option('-d', '--day', prompt=True, prompt_required=False, default="today")
def scaffold(day):
    """ Setup a single day folder """
    from aoc_2022.toolkit import scaffold_day

    day = get_day(day)
    scaffold_day(day)




@cli.command()
@click.option('-d', '--day', prompt=True, prompt_required=False, default="today")

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
    import re
    match = re.match(r"(\d{1,2}|today)?:(1|2)?", path)
    if not match:
        click.echo("Invalid path")
        return
    
    
    day, puzzle = match.groups()

    if day is None and puzzle is None:
        click.echo("Invalid path")
        return

    if day is None:
        day = "today"
    if puzzle is None:
        puzzle = "1"
    prefix = f"[ {'LOCAL' if not remote else 'REMOTE'} ] "
    try:
        table = {"1": "first", "2": "second"}

        day = cast(int,get_day(day))
        puzzle = table[puzzle]
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





if __name__ == "__main__":
    cli()
