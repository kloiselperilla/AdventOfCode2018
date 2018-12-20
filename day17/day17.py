import re
from collections import defaultdict


def stream_fill(xi, yi, grid, ranges):
    y = yi
    maxy = ranges[3]
    while y <= maxy:
        below = grid[xi, y + 1]
        if below == '.':
            # Go down
            grid[xi, y + 1] = '|'
            y += 1

        elif below in '#~':
            # Spread Left
            x = xi - 1
            spill = False
            spill_l = False
            left_limit = None
            while grid[x, y] not in '#~':
                # If you're on top of cusp, spill
                if grid[x, y + 1] in '#~' and grid[x - 1, y + 1] not in '#~' and grid[x - 1, y] not in '#~':
                    spill = True
                    spill_l = True
                    left_limit = x - 1
                    break
                else:
                    x -= 1
            if not spill:
                left_limit = x + 1

            # Spread Right
            x = xi + 1
            spill_r = False
            right_limit = None
            while grid[x, y] not in '#~':
                # If you're on top of cusp, spill
                if grid[x, y + 1] in '#~' and grid[x + 1, y + 1] not in '#~' and grid[x + 1, y] not in '#~':
                    spill = True
                    spill_r = True
                    right_limit = x + 1
                    break
                else:
                    x += 1
            if not spill_r:
                right_limit = x - 1
            # Even if you didn't spill off this end, you still fill with | if any spill
            for xj in range(left_limit, right_limit + 1):
                grid[xj, y] = '|' if spill else '~'

            # Rise with water level
            if not spill:
                grid[xi, y] = '~'

            else:
                if spill_l:
                    stream_fill(left_limit, y, grid, ranges)
                if spill_r:
                    stream_fill(right_limit, y, grid, ranges)
            y -= 1

        elif below == '|':
            # Done
            return


def fill(filename):
    with open(filename, 'r') as f:
        lines = map(lambda s: re.findall(r'(^.|\d+)', s), f.readlines())

    grid = defaultdict(lambda: '.')
    for ori, a, b, c in lines:
        if ori == 'x':
            x = int(a)
            yi = int(b)
            yf = int(c) + 1
            for y in range(yi, yf):
                grid[(x, y)] = '#'
        else:
            y = int(a)
            xi = int(b)
            xf = int(c) + 1
            for x in range(xi, xf):
                grid[(x, y)] = '#'

    minx = min(grid, key=lambda key: key[0])[0]
    maxx = max(grid, key=lambda key: key[0])[0]
    miny = min(grid, key=lambda key: key[1])[1]
    maxy = max(grid, key=lambda key: key[1])[1]
    ranges = (minx, maxx, miny, maxy)
    grid[(500, 0)] = '+'
    stream_fill(500, 0, grid, ranges)
    return grid, ranges


def num_water(filename):
    grid, ranges = fill(filename)
    miny = ranges[2]
    maxy = ranges[3]

    return sum(grid[k] in '|~' for k in grid if miny <= k[1] <= maxy)
    # print_grid(grid, ranges)


def num_water_left(filename):
    grid, ranges = fill(filename)
    miny = ranges[2]
    maxy = ranges[3]

    return sum(grid[k] == '~' for k in grid if miny <= k[1] <= maxy)
    # print_grid(grid, ranges)


def print_grid(grid, ranges):
    for y in range(0, ranges[3] + 1):
        line_str = ''
        for x in range(ranges[0], ranges[1] + 1):
            line_str += grid[(x, y)]
        print(line_str)


def solve_a():
    print('a:', num_water('input.txt'))


def solve_b():
    print('b:', num_water_left('input.txt'))


def ex():
    num_water('inex.txt')


if __name__ == '__main__':
    solve_b()
