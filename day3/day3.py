from itertools import combinations
from collections import defaultdict
import re

overlap = set()

class Rectangle():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def collides(self, other):
        if self.x + self.width >= other.x and self.y + self.height >= other.y:
            # Bottom right
            return 0
        elif self.x + self.width >= other.x and other.y + other.height >= self.y:
            # Top right
            return 1
        elif other.x + other.width >= self.x and self.y + self.height >= other.y:
            # Bottom left
            return 2
        elif other.x + other.width >= self.x and other.y + other.height >= self.y:
            # Top left
            return 3
        else:
            return -1


def find_overlap(rect_a, rect_b):
    corner = rect_a.collides(rect_b)
    if corner != -1:
        if corner == 0:
            for x in range(rect_b.x, rect_a.x + rect_a.width + 1):
                for y in range(rect_b.y, rect_a.y + rect_a.height + 1):
                    overlap.add((x, y))
        elif corner == 1:
            for x in range(rect_b.x, rect_a.x + rect_a.width + 1):
                for y in range(rect_a.y, rect_b.y + rect_b.height + 1):
                    overlap.add((x, y))
        elif corner == 2:
            for x in range(rect_a.x, rect_b.x + rect_b.width + 1):
                for y in range(rect_b.y, rect_a.y + rect_a.height + 1):
                    overlap.add((x, y))
        elif corner == 3:
            for x in range(rect_a.x, rect_b.x + rect_b.width + 1):
                for y in range(rect_a.y, rect_b.y + rect_b.height + 1):
                    overlap.add((x, y))





def parse_input(inp):
    rects = []
    for i in inp:
        at = comma = colon = ex = 0
        for j in range(len(i)):
            if i[j] == '@':
                at = j
            elif i[j] == ',':
                comma = j
            elif i[j] == ':':
                colon = j
            elif i[j] == 'x':
                ex = j
        x = int(i[at + 2:comma])
        y = int(i[comma + 1: colon])
        width = int(i[colon + 2:ex])
        height = int(i[ex + 1:])
        rects.append(Rectangle(x, y, width, height))
    return rects


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        # rects = parse_input(f.read().strip().split('\n'))
        data = f.read().strip().split('\n')

    m = defaultdict(list)
    overlaps = {}
    # TODO: VALUABLE
    claims = map(lambda s: map(int, re.findall(r'\d+', s)), data)
    for (claim_number, start_x, start_y, width, height) in claims:
        overlaps[claim_number] = set()
        for i in range(start_x, start_x + width):
            for j in range(start_y, start_y + height):
                if m[(i, j)]:
                    for number in m[(i, j)]:
                        overlaps[number].add(claim_number)
                        overlaps[claim_number].add(number)
                m[(i, j)].append(claim_number)

    print(len([k for k in m if len(m[k]) > 1]))
    print([k for k in overlaps if len(overlaps[k]) == 0])


    # for pair in combinations(rects, 2):
    #     find_overlap(pair[0], pair[1])
    #
    # print(len(overlap))
