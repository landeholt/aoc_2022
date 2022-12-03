from aoc_2022.toolkit import get_local_input

data, results = get_local_input(2)

def test_first():
    from aoc_2022.day02.core import first
    assert str(first(data)) == results['first']

def test_second():
    from aoc_2022.day02.core import second
    assert str(second(data)) == results['second']