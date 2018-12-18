from typing import NamedTuple
from dataclasses import dataclass
import enum
import itertools
import collections

# Needs to be x, y to sort correctly
class Pt(NamedTuple('Pt', [('y', int), ('x', int)])):
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    @property
    def nb4(self):
        return [self + d for d in [Pt(0, 1), Pt(1, 0), Pt(0, -1), Pt(-1, 0)]]

class Team(enum.Enum):
    ELF = enum.auto()
    GOBLIN = enum.auto()

@dataclass
class Unit:
    team: Team
    position: Pt
    hp: int = 200
    alive: bool = True
    power: int = 3

class ElfDied(Exception):
    pass

class Grid(dict):
    def __init__(self, lines, power=3):
        super().__init__()

        self.units = []

        for i, line in enumerate(lines):
            for j, el in enumerate(line):
                # Only care about points when they are walls
                self[Pt(i, j)] = el == '#'

                # Add units
                if el in 'EG':
                    self.units.append(Unit(
                        team={'E': Team.ELF, 'G': Team.GOBLIN}[el],
                        position=Pt(i, j),
                        power={'E': power, 'G': 3}[el]
                    ))

    def play(self, elf_death=False):
        rounds = 0
        while True:
            if self.round(elf_death=elf_death):
                break
            rounds += 1
        return rounds * sum(unit.hp for unit in self.units if unit.alive)

    def round(self, elf_death=False):
        for unit in sorted(self.units, key=lambda unit: unit.position):
            if unit.alive:
                if self.move(unit, elf_death=elf_death):
                    return True

    def move(self, unit, elf_death=False):
        targets = [target for target in self.units if unit.team != target.team and target.alive]
        occupied = set(u2.position for u2 in self.units if u2.alive and unit != u2)

        if not targets:
            return True

        in_range = set(pt for target in targets for pt in target.position.nb4 if not self[pt] and pt not in occupied)

        # Not already next to them
        if not unit.position in in_range:
            move = self.find_move(unit.position, in_range)

            if move:
                unit.position = move

        # Get all available targets to attack
        opponents = [target for target in targets if target.position in unit.position.nb4]

        # Attack target in range with lowest hp
        if opponents:
            target = min(opponents, key=lambda unit: (unit.hp, unit.position))

            target.hp -= unit.power

            if target.hp <= 0:
                target.alive = False
                if elf_death and target.team == Team.ELF:
                    raise ElfDied()

    def find_move(self, position, targets):
        # This is a BFS, keeping track of each node's parent
        visiting = collections.deque([(position, 0)])
        # Holds info of parent node
        meta = {position: (0, None)}
        seen = set()
        occupied = {unit.position for unit in self.units if unit.alive}

        while visiting:
            pos, dist = visiting.popleft()
            for nb in pos.nb4:
                if self[nb] or nb in occupied:
                    continue
                # Add node and info on which node led to this
                if nb not in meta or meta[nb] > (dist + 1, pos):
                    meta[nb] = (dist + 1, pos)
                if nb in seen:
                    continue
                if not any(nb == visit[0] for visit in visiting):
                    visiting.append((nb, dist + 1))
            seen.add(pos)

        # Find closest nb4; if none exists, don't move
        try:
            min_dist, closest = min((dist, pos) for pos, (dist, parent) in meta.items() if pos in targets)
        except ValueError:
            return

        # Iterate backwards from target location to see which move was first
        while meta[closest][0] > 1:
            closest = meta[closest][1]

        return closest

# lines = open('input.txt').read().splitlines()
# 
# grid = Grid(lines)
# 
# print('part 1:', grid.play())
# 
# for power in itertools.count(4):
#     try:
#         outcome = Grid(lines, power).play(elf_death=True)
#     except ElfDied:
#         continue
#     else:
#         print('part 2:', outcome)
#         break

a = [Pt(1, 2), Pt(1, 5), Pt(6, 8)]
print(sorted(a))