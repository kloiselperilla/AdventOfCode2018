def check_nb8(map_grid, loc):
    x, y = loc
    state = map_grid[(x, y)]
    dirs = [(x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x, y - 1),
            (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1)]
    nb8 = ''.join([map_grid[d] for d in dirs if d in map_grid])

    if state == '.':
        if nb8.count('|') >= 3:
            return '|'
        else:
            return '.'
    elif state == '|':
        if nb8.count('#') >= 3:
            return '#'
        else:
            return '|'
    elif state == '#':
        if nb8.count('#') >= 1 and nb8.count('|') >= 1:
            return '#'
        else:
            return '.'
    else:
        print('SOMETHING HAS GONE WRONG')


def time_step(map_grid):
    new_grid = {}
    for loc in map_grid:
        new_grid[loc] = check_nb8(map_grid, loc)

    return new_grid


def print_grid(grid):
    for y in range(50):
        line_str = ''
        for x in range(50):
            line_str += grid[(x, y)]
        print(line_str)
    print()


def lumber_sim(filename, turns):
    with open(filename) as f:
        map_str = f.read().strip().split('\n')

    map_grid = {}
    for y, row in enumerate(map_str):
        for x, c in enumerate(row):
            map_grid[(x, y)] = c

    # print_grid(map_grid)
    for t in range(turns):
        # if t % 1000 == 0:
        #     print(t)
        # time.sleep(1)
        map_grid = time_step(map_grid)
        if t > 500:
            print(t + 1, sum(map_grid[c] == '|' for c in map_grid) * \
                  sum(map_grid[c] == '#' for c in map_grid), (1000000000 - (t + 1)) % 35)
        # print_grid(map_grid)

    return sum(map_grid[c] == '|' for c in map_grid) * \
           sum(map_grid[c] == '#' for c in map_grid)


def solve_a():
    print('a:', lumber_sim('input.txt', 10))


def solve_b():
    print('b:', lumber_sim('input.txt', 1000000000))


if __name__ == '__main__':
    solve_b()

# T = 35

# We need to know what part of the phase 1000000000 will be on
# If we find the points whose distance from 1000000000 are divisible by 35, we should have our answer


