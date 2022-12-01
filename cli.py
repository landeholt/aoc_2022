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


if __name__ == "__main__":
    cli()
