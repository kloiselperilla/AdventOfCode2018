from itertools import accumulate


def toInt(str):
    return int(str[1:]) if str[0] == '+' else int(str[1:]) * -1


def first_twice(series):
    s = set()
    val = 0
    s.add(0)
    while 1:
        for i in series:
            val += i
            if val in s:
                return val
            s.add(val)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        input_str = f.read().strip()

    input_list = input_str.split('\n')

    results = list(map(toInt, input_list))

    sum = sum(results)

    twice = first_twice(results)

    print(sum)
    print(twice)