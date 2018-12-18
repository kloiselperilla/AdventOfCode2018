import time

class Node:
    def __init__(self, val, prev):
        self.val = val
        self.next = None
        self.prev = prev


class MyDeque:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, val):
        new_node = Node(val, self.tail)
        if self.head is None:
            self.head = new_node
        if self.tail is not None:
            self.tail.next = new_node
        self.tail = new_node
        self.length += 1

    def last_10_from_n(self, n):
        i = self.length
        nd = self.tail
        while i > n + 10:
            nd = nd.prev
            i -= 1
        arr = []
        while i > n:
            arr.insert(0, nd.val)
            nd = nd.prev
            i -= 1
        return arr

    def last(self, n):
        i = 0
        nd = self.tail
        arr = []
        while i < n:
            arr.insert(0, nd.val)
            nd = nd.prev
            i += 1
        return arr

    def __len__(self):
        return self.length


def add_to_board(cur1: Node, cur2: Node, board: MyDeque):
    res = cur1.val + cur2.val
    if res >= 10:
        board.append(res // 10)
    board.append(res % 10)


def forward(cur: Node, board: MyDeque):
    n = cur.val + 1
    for _ in range(n):
        if cur.next:
            cur = cur.next
        else:
            cur = board.head
    return cur


def find_ten(inp):
    board = MyDeque()
    board.append(3)
    board.append(7)
    cur1 = board.head
    cur2 = board.tail
    # t = 0
    while len(board) < int(inp) + 10:
        # if t % 50000 == 0:
        #     print(t)
        # t += 1
        add_to_board(cur1, cur2, board)
        cur1 = forward(cur1, board)
        cur2 = forward(cur2, board)
    return ''.join(str(v) for v in board.last_10_from_n(int(inp)))


def find_inp(inp):
    board = MyDeque()
    board.append(3)
    board.append(7)
    cur1 = board.head
    cur2 = board.tail
    # t = 0

    done = False
    while not done:
        # if t % 500000 == 0:
        #     print(t)
        # t += 1
        add_to_board(cur1, cur2, board)
        cur1 = forward(cur1, board)
        cur2 = forward(cur2, board)
        if len(board) > 7:
            last = ''.join(str(v) for v in board.last(7))
            if inp in last:
                return last.index(inp) + len(board) - 7


if __name__ == '__main__':
    # My solution with some custom queue
    start = time.time()
    print('a:', find_ten('633601'))
    end = time.time()
    print(end - start)

    start = time.time()
    print('b:', find_inp('633601'))
    end = time.time()
    print(end - start)

    # Reddit solution: Apparently strings are way faster :/
    # recipes = '633601'
    # score = '37'
    # elf1 = 0
    # elf2 = 1
    # while recipes not in score[-7:]:
    #     score += str(int(score[elf1]) + int(score[elf2]))
    #     elf1 = (elf1 + int(score[elf1]) + 1) % len(score)
    #     elf2 = (elf2 + int(score[elf2]) + 1) % len(score)
    # 
    # print('Part 1:', score[int(recipes):int(recipes) + 10])
    # print('Part 2:', score.index(recipes))
