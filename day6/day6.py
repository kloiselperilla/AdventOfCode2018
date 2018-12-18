import re
from collections import Counter

def test_a():
    coord = [[1,1], [1,6],[8,3],[3,4],[5,5],[8,9]]


def dist(a, b):
    # print('{} - {} = {}'.format(a, b, abs(a[0] - b[0]) + abs(a[1] - b[1])))
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def on_edges(pt, edges):
    return pt[0] == edges[0] or pt[0] == edges[1] or pt[1] == edges[2] or pt[1] == edges[3]


def find_closest(pt, coord, areas, inf, edges):
    # print(min([dist(pt, c) for c in coord], key=coord.__getitem__))
    mindex = -1
    min = -1
    total = 0
    for i in range(len(coord)):
        d = dist(pt, coord[i])
        total += d
        if min == -1 or d < min:
            mindex = i
            min = d
        elif d == min:
            mindex = -1 # same distance
    if mindex != -1:
        if mindex not in areas:
            areas[mindex] = 1
        else:
            areas[mindex] += 1
        if on_edges(pt, edges):
            inf.append(mindex)
    return mindex, total



if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        coord = list(map(lambda s: tuple(map(int, re.findall(r'\d+', s))), f.read().strip().split('\n')))

    # [print(x, y) for x, y in coord]

    minx = miny = -1
    maxx = maxy = -1
    for x, y in coord:
        if minx == -1 or x < minx:
            minx = x
        if maxx == -1 or x > maxx:
            maxx = x
        if miny == -1 or y < miny:
            miny = y
        if maxy == -1 or y > maxy:
            maxy = y

    edges = (minx, maxx, miny, maxy)
    rangex = maxx + 1 - minx
    rangey = maxy + 1 - miny
    areas = {}
    closest = {}
    inf = []
    close_area = 0

    # TODO: Solution had closest be a grid
    for y in range(rangey):
        for x in range(rangex):
            closest[(x, y)], total_d = find_closest((x + minx, y + miny), coord, areas, inf, edges)
            if total_d < 10000:
                close_area += 1

    # max = 0
    # for a in areas:
    #     if a not in inf and areas[a] > max:
    #         max = areas[a]

    # print('a:', max)
    # TODO: Make note of the Counter, most_common, next trick
    print('a:', next(i[1] for i in Counter(closest.values()).most_common() if i[0] not in inf))
    print('b:', close_area)

