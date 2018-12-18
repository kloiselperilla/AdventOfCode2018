import re
import matplotlib.pyplot as plt
import numpy as np

plt.interactive(False)
if __name__ == '__main__':
    with open('input.txt', 'r') as f:

        pts = map(lambda s : map(int, re.findall(r'-?\d+', s)), f.read().strip().split('\n'))

    vec_data = np.array([(x, y, vx, vy) for x, y, vx, vy in pts])
    x = vec_data[:, 0]
    y = vec_data[:, 1]
    vx = vec_data[:, 2]
    vy = vec_data[:, 3]

    for _ in range(10375):
        x = np.add(x, vx)
        y = np.add(y, vy)
        plt.show()

    axes = plt.gca()

    axes.set_xlim(100, 300)
    axes.set_ylim(100, 300)
    axes.invert_yaxis()
    line, = axes.plot(x, y, '.')
    plt.show()

