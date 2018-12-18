import os
import time
import sys

UNIT_HEALTH = 200
UNIT_ATTACK = 3

class Unit:
    def __init__(self, pos: complex, is_elf):
        self.is_elf = is_elf
        self.pos = pos
        self.hp = UNIT_HEALTH
        self.atk = UNIT_ATTACK
        self.icon = 'E' if self.is_elf else 'G'
        self.alive = True

    def move(self, dest, battle_map):
        battle_map[int(self.pos.imag)][int(self.pos.real)] = '.'
        self.pos = dest
        battle_map[int(dest.imag)][int(dest.real)] = self

    def die(self, battle_map):
        battle_map[int(self.pos.imag)][int(self.pos.real)] = '.'
        self.alive = False

    def attack(self, other, battle_map):
        other.hp -= self.atk
        # print('{} attacks {}'.format(repr(self), repr(other)))
        if other.hp <= 0:
            # print('DEAD')
            other.die(battle_map)

    def attack_phase(self, battle_map):
        enemies = []
        x, y = int(self.pos.real), int(self.pos.imag)

        c = battle_map[y - 1][x]
        if isinstance(c, Unit) and c.is_elf != self.is_elf:
            enemies.append(c)

        c = battle_map[y][x - 1]
        if isinstance(c, Unit) and c.is_elf != self.is_elf:
            enemies.append(c)

        c = battle_map[y + 1][x]
        if isinstance(c, Unit) and c.is_elf != self.is_elf:
            enemies.append(c)

        c = battle_map[y][x + 1]
        if isinstance(c, Unit) and c.is_elf != self.is_elf:
            enemies.append(c)

        if enemies:
            target = sorted(enemies, key=lambda e: (e.hp, e.pos.imag, e.pos.real))[0]
            self.attack(target, battle_map)

    def find_first_move(self, nrst, parents):
        if nrst == self.pos:
            return None
        curr = nrst
        parent = parents[nrst]
        while parent != self.pos:
            curr = parent
            parent = parents[curr]
        return curr

    def try_adj(self, battle_map, queue, visited, pos: complex, direction: complex, parents):
        if (pos + direction) not in visited:
            parents[pos + direction] = pos
            x, y = int((pos + direction).real), int((pos + direction).imag)
            c = battle_map[y][x]
            if c == '.':
                queue.append(pos + direction)
                visited[pos + direction] = True
            elif isinstance(c, Unit) and c.is_elf != self.is_elf:
                return pos
        return None

    def find_nearest_reachable_in_range(self, battle_map):
        # BFS
        visited = {}
        queue = [self.pos]
        visited[self.pos] = True
        parents = {}

        while queue:
            pos = queue.pop(0)

            # For reading order: up, left, right, down
            # Up
            adj = self.try_adj(battle_map, queue, visited, pos, -1j, parents)
            if adj:
                first_move = self.find_first_move(adj, parents)
                return adj, first_move

            # Left
            adj = self.try_adj(battle_map, queue, visited, pos, -1, parents)
            if adj:
                first_move = self.find_first_move(adj, parents)
                return adj, first_move

            # Right
            adj = self.try_adj(battle_map, queue, visited, pos, +1, parents)
            if adj:
                first_move = self.find_first_move(adj, parents)
                return adj, first_move

            # Down
            adj = self.try_adj(battle_map, queue, visited, pos, +1j, parents)
            if adj:
                first_move = self.find_first_move(adj, parents)
                return adj, first_move
        return None, None

    def __repr__(self):
        return '{{{}: ({}, {}), HP: {}}}'.format(self.icon, int(self.pos.real), int(self.pos.imag), self.hp)
        # return '{}'.format(self.icon)

    def __str__(self):
        return '{}'.format(self.icon)


def print_map(battle_map):
    for row in battle_map:
        print(''.join([str(i) for i in row]))


def remove_dead(goblins, elves):
    # print('dead:', [u for u in goblins+elves if not u.alive])
    return [g for g in goblins if g.alive], [e for e in elves if e.alive]


def time_step(battle_map, goblins, elves):
    units = sorted(goblins + elves, key=lambda u: (u.pos.imag, u.pos.real))
    for unit in units:
        if unit.alive:
            if unit.is_elf and not goblins or not unit.is_elf and not elves:
                return goblins, elves, True
            nrst, first_move = unit.find_nearest_reachable_in_range(battle_map)
            if nrst:
                if first_move:
                    unit.move(first_move, battle_map)
                if nrst == unit.pos:
                    unit.attack_phase(battle_map)
            goblins, elves = remove_dead(goblins, elves)
        # units = sorted(goblins + elves, key=lambda u: (u.pos.imag, u.pos.real))
    return goblins, elves, False

def get_map_and_units(file):
    goblins = []
    elves = []
    with open(file, 'r') as f:
        battle_map = []
        for y, line in enumerate(f.readlines()):
            battle_map.append([])
            for x, c in enumerate(line.strip()):
                if c == 'G':
                    gobbo = Unit(x + y * 1j, is_elf=False)
                    goblins.append(gobbo)
                    battle_map[y].append(gobbo)
                elif c == 'E':
                    elf = Unit(x + y * 1j, is_elf=True)
                    elves.append(elf)
                    battle_map[y].append(elf)
                else:
                    battle_map[y].append(c)
    return battle_map, goblins, elves


def run_sim(battle_map, goblins, elves):
    print_map(battle_map)
    t = 0
    goblins, elves, done = time_step(battle_map, goblins, elves)
    time.sleep(0.5)
    print_map(battle_map)
    # print([repr(g) for g in goblins])
    # print([repr(e) for e in elves])
    while not done:
        t += 1
        print_map(battle_map)
        goblins, elves, done = time_step(battle_map, goblins, elves)
        # print(t)
        # print([repr(g) for g in goblins])
        # print([repr(e) for e in elves])
        time.sleep(0.5)

    print()
    print_map(battle_map)
    print('THE BATTLE IS OVER')
    if goblins:
        print('GOBLINS WIN')
        print([u.hp for u in goblins])
        hpsum = sum([u.hp for u in goblins])
    else:
        print('ELVES WIN')
        hpsum = sum([u.hp for u in elves])
    print('Turns:', t)
    print('Hpsum', hpsum)
    print('a:', hpsum * t)

def ex0():
    battle_map, goblins, elves = get_map_and_units('inex0.txt')
    run_sim(battle_map, goblins, elves)

def ex1():
    battle_map, goblins, elves = get_map_and_units('inex1.txt')
    run_sim(battle_map, goblins, elves)

def ex2():
    battle_map, goblins, elves = get_map_and_units('inex2.txt')
    run_sim(battle_map, goblins, elves)

def ex3():
    battle_map, goblins, elves = get_map_and_units('inex3.txt')
    run_sim(battle_map, goblins, elves)

def ex4():
    battle_map, goblins, elves = get_map_and_units('inex4.txt')
    run_sim(battle_map, goblins, elves)

def ex5():
    battle_map, goblins, elves = get_map_and_units('inex5.txt')
    run_sim(battle_map, goblins, elves)


def solve_a():
    battle_map, goblins, elves = get_map_and_units('input.txt')
    run_sim(battle_map, goblins, elves)


if __name__ == '__main__':
    # ex5()
    solve_a()
