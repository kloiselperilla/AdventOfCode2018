import re
from collections import OrderedDict

def util(v, graph, visited, stack):
    if v not in visited:
        visited.append(v)
    if v in graph:
        for u in sorted(graph[v], reverse=True):
            if u not in visited:
                util(u, graph, visited, stack)

    stack.insert(0, v)


def top_sort(graph):
    visited = []
    stack = []
    for v in sorted(graph, reverse=True):
        if v not in visited:
            util(v, graph, visited, stack)
    return stack


def ready(c, need, accounted, busy, t):
    if c not in need:
        return True
    for v in need[c]:
        if v not in accounted:
            return False
        for w in busy:
            if w[0] == v and t < w[1]:
                return False
    return True


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        dep = list(map(lambda s: tuple(map(str.strip, re.findall(r'\s[A-Z]\s', s))), f.readlines()))

    need = {}
    graph = {}
    for pre, post in dep:
        # print(pre, post)
        lst = graph.get(pre, None)
        if pre not in graph:
            graph[pre] = [post]
        else:
            graph[pre].append(post)
        if post not in graph:
            graph[post] = []
        if post not in need:
            need[post] = [pre]
        else:
            need[post].append(pre)
        if pre not in need:
            need[pre] = []

    order = ''.join(top_sort(graph))
    print('a:', order)
    print('GRAPH')
    [print(l, graph[l]) for l in sorted(graph)]
    print('NEED')
    [print(l, graph[l]) for l in sorted(need)]
    WORKERS = 5
    busy = [['', 0]] * WORKERS

    print(busy[0][1])
    t = 0
    i = 0
    done = False
    accounted = []
    while i < len(order):
        go = True
        for w in range(WORKERS):
            # print(busy)
            if t >= busy[w][1] and ready(order[i], need, accounted, busy, t):
                go = False
                busy[w] = [order[i], ord(order[i].lower()) - 96 + 60 + t]
                print('Worker', w, 'working on', order[i], ': @', t)
                accounted.append(order[i])
                i += 1
                if i == len(order):
                    break
        if go:
            t += 1

    print('b:', max(busy, key=lambda item:item[1])[1])
    print(busy)
