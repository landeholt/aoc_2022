from aoc_2022.toolkit import get_local_input

data, first_result, second_result = get_local_input(1)
def test_first():
    from aoc_2022.day01.core import first
    assert str(first(data)) == first_result



def test_second():
    from aoc_2022.day01.core import second
    assert str(second(data)) == second_result
