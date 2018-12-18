import re
from collections import deque

def ex():
    with open('inex.txt', 'r') as f:
        init = re.findall(r'[#.]+', f.readline())[0]
        # print(init)
        f.readline()
        # print(f.readlines())
        rules = list(map(lambda s : list(map(str.strip, re.findall(r'[#.]+', s))), f.readlines()))

    set = ['#', '.']
    print(len(rules))
    for a in set:
        for b in set:
            for c in set:
                for d in set:
                    for e in set:
                        comb = ''.join([a,b,c,d,e])
                        for rule in rules:
                            if rule[0] == comb:
                                break
                        else:
                            print(comb)
                            rules.append((comb, '.'))
    print(len(rules))
    print(grow(init, rules).count('#'))
    print(sum([i - 20 for i, e in enumerate(grow(init, rules)) if e == '#']))


def grow(init, rules, gen):
    plants = ['.'] * gen + list([plant for plant in init]) + ['.'] * gen
    for t in range(gen):
        changing = {}
        plant_str = ''.join(plants)
        for config, out in rules:
            for i in range(len(plant_str)):
                if plant_str[i:i + 5] == config:
                    changing[i + 2] = out

        for ix in changing:
            plants[ix] = changing[ix]
    return plants


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        init = re.findall(r'[#.]+', f.readline())[0]
        # print(init)
        f.readline()
        # print(f.readlines())
        rules = list(map(lambda s : list(map(str.strip, re.findall(r'[#.]+', s))), f.readlines()))

    last = sum([i - 20 for i, e in enumerate(grow(init, rules, 20)) if e == '#'])
    print('a:', last)

    diff = 0
    for gen in range(40, 220, 20):
        new_last = sum([i - gen for i, e in enumerate(grow(init, rules, gen)) if e == '#'])
        diff = new_last - last
        print(new_last, diff, gen)

        last = new_last

    print(diff, last)

    # Looks like it consistently increases after a while
    # Put that shit into point slope:
    # y - 17480 = (1600/20)(x - 200)
    m = diff // 20
    print('b:', m * 50000000000 - (m * 200) + last)