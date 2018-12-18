import re
from collections import deque

def ex1():
    players = 9
    last_val = 25
    print(get_high_score(players, last_val))

def ex2():
    players, last_val = map(int, re.findall(r'\d+', '10 players; last marble is worth 1618 points'))
    print(get_high_score(players, last_val))

def ex3():
    players, last_val = map(int, re.findall(r'\d+', '13 players; last marble is worth 7999 points'))
    print(get_high_score(players, last_val))

def ex4():
    players, last_val = map(int, re.findall(r'\d+', '17 players; last marble is worth 1104 points'))
    print(get_high_score(players, last_val))

def ex5():
    players, last_val = map(int, re.findall(r'\d+', '10 players; last marble is worth 1618 points'))
    pass
def ex6():
    players, last_val = map(int, re.findall(r'\d+', '10 players; last marble is worth 1618 points'))
    pass


def get_high_score(players, last_val):
    scores = [0] * players
    # XXX: NOTE that deque is far more efficient than list for this
    # XXX: when going around in a circle and removing and adding as you go, deques are the way to go
    circle = deque([0])
    for i in range(1, last_val + 1):
        if i % 23 == 0:
            circle.rotate(7)
            scores[(i - 1) % players] += i + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(i)
    return scores


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        players, last_val = map(int, re.findall(r'\d+', f.read().strip()))

    print('a:', max(get_high_score(players, last_val)))
    print('b:', max(get_high_score(players, last_val * 100)))
