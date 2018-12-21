def addr(registers, a, b, c):
    result = registers[::]
    result[c] = result[a] + result[b]
    return result


def addi(registers, a, b, c):
    result = registers[::]
    result[c] = result[a] + b
    return result


def mulr(registers, a, b, c):
    result = registers[::]
    result[c] = result[a] * result[b]
    return result


def muli(registers, a, b, c):
    result = registers[::]
    result[c] = result[a] * b
    return result


def banr(registers, a, b, c):
    result = registers[::]
    result[c] = result[a] & result[b]
    return result


def bani(registers, a, b, c):
    result = registers[::]
    result[c] = result[a] & b
    return result


def borr(registers, a, b, c):
    result = registers[::]
    result[c] = result[a] | result[b]
    return result


def bori(registers, a, b, c):
    result = registers[::]
    result[c] = result[a] | b
    return result


def setr(registers, a, b, c):
    result = registers[::]
    result[c] = result[a]
    return result


def seti(registers, a, b, c):
    result = registers[::]
    result[c] = a
    return result


def gtir(registers, a, b, c):
    result = registers[::]
    result[c] = bool(a > result[b])
    return result


def gtri(registers, a, b, c):
    result = registers[::]
    result[c] = bool(result[a] > b)
    return result


def gtrr(registers, a, b, c):
    result = registers[::]
    result[c] = bool(result[a] > result[b])
    return result


def eqir(registers, a, b, c):
    result = registers[::]
    result[c] = bool(a == result[b])
    return result


def eqri(registers, a, b, c):
    result = registers[::]
    result[c] = bool(result[a] == b)
    return result


def eqrr(registers, a, b, c):
    result = registers[::]
    result[c] = bool(result[a] == result[b])
    return result


OPERATIONS = [
    addr, addi,
    mulr, muli,
    banr, bani,
    borr, bori,
    setr, seti,
    gtir, gtri, gtrr,
    eqir, eqri, eqrr
]

# WAY TOO SLOW
def solve_b():
    with open('input.txt') as f:
        instructions = f.read().strip().split('\n')

    ip_reg = int(instructions.pop(0).split()[1])
    no_instr = len(instructions)

    regs = [1, 0, 0, 0, 0, 0]

    while regs[ip_reg] in range(0, no_instr):
        inst = instructions[regs[ip_reg]].split()
        func = [i for i in OPERATIONS if i.__name__ == inst[0]][0]
        src1 = int(inst[1])
        src2 = int(inst[2])
        dst = int(inst[3])
        regs = func(regs, src1, src2, dst)
        regs[ip_reg] += 1

    print(regs)


def asm_func(n):
    # n = 948
    c = 0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i*j == n:
                c += i
        print(i)
    return c


def solve_a():
    # int c = 0;
    # for (int i = 1; i <= 1993; i++){
    #     for (int j = 1; j <= 1993; j++) {
    #         if (i*j == 1993) {
    #             c += i;
    #         }
    #     }
    # }
    # return c;
    with open('input.txt') as f:
        instructions = f.read().strip().split('\n')

    ip_reg = int(instructions.pop(0).split()[1])
    no_instr = len(instructions)
    # print(no_instr)

    regs = [0, 0, 0, 0, 0, 0]

    while regs[ip_reg] in range(0, no_instr):
        inst = instructions[regs[ip_reg]].split()
        func = [i for i in OPERATIONS if i.__name__ == inst[0]][0]
        src1 = int(inst[1])
        src2 = int(inst[2])
        dst = int(inst[3])
        regs = func(regs, src1, src2, dst)
        # print(regs[ip_reg], regs)
        print(regs)
        if regs[ip_reg] == 25:
            break
        regs[ip_reg] += 1

    print(regs)



from functools import reduce

# Thank you stack overflow
def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


if __name__ == '__main__':
    print('a:', sum(factors(948)))
    print('b:', sum(factors(10551348)))
