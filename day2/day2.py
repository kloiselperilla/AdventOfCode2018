def two_three_count(list):
    c2 = 0
    c3 = 0
    for i in list:
        f2 = False
        f3 = False
        for c in i:
            cnt = i.count(c)
            if cnt == 2:
                f2 = True
            elif cnt == 3:
                f3 = True
            if f2 and f3:
                break
        if f2:
            c2 += 1
        if f3:
            c3 += 1
    return c2, c3


def diff_by_one(word_a, word_b):
    diffs = 0
    new_word = ''
    for a, b in zip(word_a, word_b):
        if a != b:
            if diffs:
                return None
            diffs += 1
        else:
            new_word += a
    return new_word


def neighbors(list):
    for a in list:
        for b in list:
            if a != b:
                new_word = diff_by_one(a, b)
                if new_word:
                    return new_word


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        input_list = f.read().strip().split('\n')

    c2, c3 = two_three_count(input_list)
    print(c2 * c3)

    print(neighbors(input_list))