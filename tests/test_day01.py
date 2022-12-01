from aoc_2022.toolkit import get_local_input

data = get_local_input(1)

def test_first():
    from aoc_2022.day01.core import first
    assert first(data) == 24000



def test_second():
    from aoc_2022.day01.core import second
    assert second(data) == 45000
