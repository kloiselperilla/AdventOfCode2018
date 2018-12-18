import string

def match(c1, c2):
    return c1.islower() and c2.isupper() and c1.upper() == c2 or \
           c1.isupper() and c2.islower() and c2.upper() == c1


def bond(polymer):
    i = 1
    try:
        while i < len(polymer) or polymer[i] != '*':
            # for i in range(len(polymer)):
            if match(polymer[i], polymer[i - 1]):
                polymer = polymer[:i - 1] + polymer[i + 1:]
                i -= 1
            else:
                i += 1
    except (IndexError):
        print(i, len(polymer))
    return polymer


def improved_bond(polymer, prob):
    i = 1
    try:
        while i < len(polymer) or polymer[i] != '*':
            # TODO: THIS IS REALLY FITTING FOR A STACK - USE POP, etc.
            if match(polymer[i], polymer[i - 1]):
                polymer = polymer[:i - 1] + polymer[i + 1:]
                i -= 2
            elif polymer[i].lower() == prob:
                polymer = polymer[:i] + polymer[i + 1:]
                i -= 1
            else:
                i += 1
    except (IndexError):
        print(i, len(polymer))
    return polymer


# TODO: MAKE NOTE OF STACK SOLUTION AND SWAPCASE
def solution_bond(polymer):
    buf = []
    for c in polymer:
        if buf and buf[-1] == c.swapcase():
            buf.pop()
        else:
            buf.append(c)
    return len(buf)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        polymer = f.read().strip()
        # polymer += '*' # Sentinel

    # print(polymer)
    # polymer1 = bond(polymer)
    #
    # min = -1
    # for c in string.ascii_lowercase:
    #     sz = len(improved_bond(polymer, c))
    #     if min == -1 or sz <= min:
    #         min = sz
    #
    # print('a:', len(polymer1[:-1]))
    # print('b:', min - 1)


    print('a:', solution_bond(polymer))
    print('b:', min([solution_bond(polymer.replace(a, '').replace(a.upper(), ''))
                     for a in string.ascii_lowercase]))
