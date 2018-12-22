from collections import defaultdict, deque


DIRS = {'N': 1j, 'E': 1, 'S': -1j, 'W': -1}


def map_out(dir_it, grid, pos: complex):
    for d in dir_it:
        if d == '(':
            branch = pos.real + pos.imag * 1j
            go = map_out(dir_it, grid, branch)
            while go:
                # next(dir_it)
                go = map_out(dir_it, grid, branch)
            continue
        elif d == '|':
            return True
        elif d == ')':
            return False
        elif d == '$':
            return False
        else:
            pos += DIRS[d]
            grid[pos] = '|' if d in 'EW' else '-'
            if pos == (-3 + 3j):
                print('here')
            pos += DIRS[d]
            map_room(grid, pos)


def map_room(grid, pos):
    grid[pos] = '.'
    grid[pos + 1 + 1j] = '#'
    grid[pos + 1 - 1j] = '#'
    grid[pos - 1 + 1j] = '#'
    grid[pos - 1 - 1j] = '#'
    for d in DIRS.values():
        if pos + d not in grid:
            grid[pos + d] = '?'


def print_map(grid):
    minx = min(grid, key=lambda key: key.real).real
    maxx = max(grid, key=lambda key: key.real).real
    miny = min(grid, key=lambda key: key.imag).imag
    maxy = max(grid, key=lambda key: key.imag).imag

    for y in range(int(maxy), int(miny) - 1, -1):
        line_str = ''
        for x in range(int(minx), int(maxx) + 1):
            line_str += grid[x + y * 1j] if x + y * 1j in grid else ' '

        print(line_str)


def create_map(filename):
    with open(filename) as f:
        dir_str = f.read().strip()[1:]
    grid = defaultdict(lambda s: ' ')
    pos = 0 + 0j
    map_room(grid, pos)
    grid[pos] = 'X'
    dir_it = iter(dir_str)
    map_out(dir_it, grid, pos)
    grid = {k: ('#' if v == '?' else v) for k, v in grid.items()}
    return grid


def search_map(grid):
    q = deque()
    visited = []
    q.append((0 + 0j, 0))
    visited.append((0 + 0j, 0))
    while q:
        pos, doors = q.popleft()
        # print(doors)
        for d in DIRS.values():
            # been_visited = pos + 2 * d in v[0] for v in visited
            if grid[pos + d] != '#' and pos + 2 * d not in [v[0] for v in visited]:
                visited.append((pos + 2 * d, doors + 1))
                q.append((pos + 2 * d, doors + 1))
    return visited


def solve_a():
    # Step 1: Map out
    # Step 2: BFS (Which node is the last visited on the BFS)
    print('a:', search_map(create_map('input.txt'))[-1][1])


def solve_b():
    print('b:', sum(v[1] >= 1000 for v in search_map(create_map('input.txt'))))


def ex1():
    grid = create_map('inex1.txt')
    print_map(grid)

    v = search_map(grid)
    print(v[-1])

def ex0():
    grid = create_map('inex0.txt')
    print_map(grid)

    v = search_map(grid)
    print(v[-1])

def ex2():
    grid = create_map('inex2.txt')
    print_map(grid)

    v = search_map(grid)
    print(v[-1])

if __name__ == '__main__':
    # solve_a()
    solve_b()


# 8580 too low