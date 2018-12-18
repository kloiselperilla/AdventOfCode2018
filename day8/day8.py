def test_example():
    inp = iter(list(map(int, '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'.split())))
    # 138
    print(get_metadata(inp))

def test_example2():
    inp = iter(list(map(int, '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'.split())))
    # 138
    print(get_metadata_and_val(inp))

def func2(inp):
    for i in inp:
        print(i)
        break


def get_metadata(inp):
    meta_total = 0
    num_child = next(inp)
    num_meta = next(inp)
    for child in range(num_child):
        meta_total += get_metadata(inp)
    for meta in range(num_meta):
        meta_total += next(inp)
    return meta_total


def get_metadata_and_val(inp):
    meta_total = 0
    num_child = next(inp)
    num_meta = next(inp)
    child_vals = []
    meta_ixs = []
    for child in range(num_child):
        child_meta, child_val = get_metadata_and_val(inp)
        # print(child_val)
        meta_total += child_meta
        child_vals.append(child_val)
    for meta in range(num_meta):
        m = next(inp)
        meta_total += m
        meta_ixs.append(m)
    val = 0
    if num_child:
        for m in meta_ixs:
            # print('m:', m)
            if m <= len(child_vals) and m != 0:
                val += child_vals[m - 1]
    else:
        val = meta_total
    if val == 0:
        print('uh oh', num_child, num_meta, meta_total, '\n\tmetas:', meta_ixs, '\n\tchildvals:', child_vals)
    return meta_total, val


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        inp = iter(list(map(int, f.read().strip().split())))


    meta_total, root_val = get_metadata_and_val(inp)
    print('a:', meta_total)
    print('b:', root_val)

    # test_example2()