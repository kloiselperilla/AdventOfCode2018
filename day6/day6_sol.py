# TODO: Actually tho mine is way faster

data = [tuple(map(int, i.split(', '))) for i in open('input.txt').readlines()]


# print(data)
# dc = data.copy()

ls = list(zip(*data))
# [print(x, y) for x, y in data]
# print(data)

side = max(max(ls[0]), max(ls[1]))
# side = max(max(zip(*data)[0]), max(zip(*data)[1]))
squares = lambda: ((x, y) for x in range(side) for y in range(side))
distance = lambda x, y: [abs(x-i) + abs(y-j) for i, j in data]
closest = lambda x, y: next(n for n, (i, j) in enumerate(data) if not 'm' in list(locals().keys()) and locals().update({'m': min(distance(x, y))}) or abs(x-i) + abs(y-j) == locals()['m'])

eqidistant = set((x, y) for x, y in squares() if distance(x, y).count(min(distance(x, y))) > 1)
grid = {(x, y): closest(x, y) if (x, y) not in eqidistant else -1 for x, y in squares()}
inf = set(grid[x, y] for edge in range(side) for x, y in [(edge, side-1), (edge, 0), (side-1, edge), (0, edge)])

print(max(list(grid.values()).count(n) for n in range(len(data)) if n not in inf))
print(sum(sum(distance(x, y)) < 10000 for x, y in squares()))