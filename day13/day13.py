from collections import defaultdict


DIR = {'^': -1j, '>': +1, 'v': +1j, '<': -1}
NAIVE_REPLACEMENTS = {'^': '|', '>': '-', 'v': '|', '<': '-'}
TURNS = {0: -1j, 1: 1, 2: +1j}


class Cart:
    def __init__(self, x, y, c):
        self.pos = x + y * 1j
        self.direction = DIR[c]
        self.next_turn_count = 0
        self.active = True

    def __str__(self):
        return '({}) {}'.format(self.pos, self.direction)

    def __repr__(self):
        return '({}) {}'.format(self.pos, self.direction)

    def __eq__(self, other):
        return self.pos == other.pos

    def remove(self):
        self.active = False
        self.pos = -1 - 1j

    def turn(self):
        self.direction *= TURNS[self.next_turn_count]
        self.next_turn_count = (self.next_turn_count + 1) % 3

    def check_collisions(self, carts):
        for cart in carts:
            if id(self) != id(cart) and self == cart:
                return cart
        return None

    def move(self, tracks, carts):
        # Move, check for direction changes, and check for collisions
        if self.active:
            self.pos += self.direction
            pos = tracks[self.pos]
            if pos == '+':
                self.turn()
            elif pos == '/':
                self.direction *= -1j if self.direction.real else +1j
            elif pos == '\\':
                self.direction *= +1j if self.direction.real else -1j

            check = self.check_collisions(carts)
            if check:
                col_loc = (self.pos.real, self.pos.imag)
                self.remove()
                check.remove()
                return col_loc
        return False


def time_step(tracks, carts, remove=False):
    for c in sorted(carts, key=lambda cart: (cart.pos.imag, cart.pos.real)):
        loc = c.move(tracks, carts)
        if loc and not remove:
            print('a:', loc)
            return False
    return True


def get_map_and_carts(file):
    with open(file, 'r') as f:
        map_list = f.read().split('\n')
        if not map_list[-1]:
            map_list = map_list[:-1]
    carts = []
    tracks = defaultdict(lambda: "")
    for y, row in enumerate(map_list):
        for x, c in enumerate(row):
            if c in DIR:
                carts.append(Cart(x, y, c))
                map_list[y] = map_list[y][:x] + NAIVE_REPLACEMENTS[c] + map_list[y][x + 1:]
            elif c in "\\/+":
                tracks[(x + y * 1j)] = c
    return tracks, carts


def ex():
    tracks, carts = get_map_and_carts('inex.txt')
    col = False
    while not col:
        if not time_step(tracks, carts):
            col = True


def ex2():
    rail_map, carts = get_map_and_carts('inex2.txt')
    done = False
    while not done:
        time_step(rail_map, carts, remove=True)
        if len([c for c in carts if c.active]) == 1:
            print([c for c in carts if c.active][0].pos)
            done = True


def solve_a():
    rail_map, carts = get_map_and_carts('input.txt')
    done = False
    while not done:
        if not time_step(rail_map, carts):
            done = True


def solve_b():
    rail_map, carts = get_map_and_carts('input.txt')
    done = False
    while not done:
        time_step(rail_map, carts, remove=True)
        if len([c for c in carts if c.active]) == 1:
            print('b:', [c for c in carts if c.active][0].pos)
            done = True


if __name__ == '__main__':
    # ex()
    # ex2()
    solve_a()
    solve_b()


    # OTHER SOLUTIONS: while len(carts) > 1, and update carts every time step