from day1 import day1


def test_a():
    set = [1, -2, 3, 1, 1, -2]
    assert day1.first_twice(set) == 2


def test_b():
    set = [1, -1]
    assert day1.first_twice(set) == 0


def test_c():
    set = [+3, +3, +4, -2, -4]
    assert day1.first_twice(set) == 10


def test_d():
    set = [-6, +3, +8, +5, -6]
    assert day1.first_twice(set) == 5