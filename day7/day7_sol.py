from collections import defaultdict, deque

# Edges
adj = defaultdict(list)
# In-degree
level = defaultdict(int)
for line in open('input.txt'):
    words = line.split()
    x = words[1]
    y = words[7]
    adj[x].append(y)
    level[y] += 1

# for k in E:
#     E[k] = sorted(E[k])


#         add_task(k)

# time
t = 0
# Events
EV = []
# Work queue
Q = []




def add_task(x):
    Q.append(x)


def start_work():
    global Q
    while len(EV) < 5 and Q:
        Q = sorted(Q)
        x = Q.pop(0)
        print('Starting {} at {}'.format(x, t))
        EV.append((t + 61 + ord(x) - ord('A'), x))


for k in adj:
    if level[k] == 0:
        add_task(k)
start_work()

while EV or Q:
    # Remove first finished event
    t, x = min(EV, key=lambda item:item[0])
    # print(t, x)
    EV.remove((t,x))
    # EV = [y for y in EV if y != (t, x)]
    for y in adj[x]:
        level[y] -= 1
        if level[y] == 0:
            add_task(y)
    start_work()

print(t)

# for k in adj:
#     if level[k] == 0:
#         Q.append(k)
#
# ans = ""
# while Q:
#     Q = sorted(Q)
#     x = Q.pop(0)
#     ans += x
#     for y in adj[x]:
#         level[y] -= 1
#         if level[y] == 0:
#             Q.append(y)
# print(ans)
