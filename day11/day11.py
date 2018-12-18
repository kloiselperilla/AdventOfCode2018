import numpy

s_no = 5719


def power(x, y):
    id = (x + 1) + 10
    p = ((((id * (y + 1) + s_no) * id) // 100) % 10) - 5
    return p


# def grid_power(x, y, size, powers):
#     p = 0
#     for yi in range(y, y+size):
#         for xi in range(x, x+size):
#             p += powers[(xi,yi)]
#     return p
#
#
# def best_33(powers):
#     grid = {}
#
#     for y in range(1, 299):
#         for x in range(1, 299):
#             grid[(x, y)] = grid_power(x, y, 3, powers)
#
#     return grid
#
#
# def best_square(powers):
#     best = {}
#     for size in range(1, 301):
#         print(size)
#         grid = {}
#
#         for y in range(1, 302 - size):
#             for x in range(1, 302 - size):
#                 grid[(x, y)] = grid_power(x, y, size, powers)
#
#         max_p = max(grid, key=grid.get)
#
#         best[(max_p[0], max_p[1], size)] = grid[max_p]
#
#     return best
#
#
# def power_trans():
#     grid = {}
#     for y in range(1, 301):
#         for x in range(1, 301):
#             grid[(x, y)] = power(x, y)
#     return grid


if __name__ == '__main__':

    # s_no = 18
    # TODO: Note this is cool
    grid = numpy.fromfunction(power, (300, 300))

    best = {}
    for width in range(1, 301):
        # TODO: None because when x = x-width+1, it defaults to none which is the same as :, which means just grid
        # TODO: Sum is VERY powerful, don't sleep on it
        windows = sum(
            grid[x:x - width + 1 or None, y:y - width + 1 or None] for x in range(width) for y in range(width))
        # TODO: coordinate holds the convolved value of the whole window
        maximum = int(windows.max())
        location = numpy.where(windows == maximum)
        best[(location[0][0] + 1, location[1][0] + 1, width)] = maximum

    # grid = best_33(powers)
    #
    #
    # print('a:', max(grid, key=grid.get), grid[max(grid, key=grid.get)])
    #
    #
    # best = best_square(powers)
    print('b:', max(best, key=best.get), best[max(best, key=best.get)])
