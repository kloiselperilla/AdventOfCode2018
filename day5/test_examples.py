from day5 import day5


def test_a():
    poly = 'aA*'
    assert day5.bond(poly) == '*'


def test_b():
    poly = 'aAa*'
    assert day5.bond(poly) == 'a*'


def test_c():
    poly = 'ab*'
    assert day5.bond(poly) == 'ab*'


def test_d():
    poly = 'baABc*'
    assert day5.bond(poly) == 'c*'

def test_e():
    poly = 'wNnJZzjXxlLrWwbBaARdaADWfmMZzFDdKCcQTCaA*'
    assert day5.bond(poly) == 'KQTC*'