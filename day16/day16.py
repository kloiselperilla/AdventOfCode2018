import re
from collections import defaultdict


def list_map(f, s):
    return list(map(f, s))
"""
Addition:
addr (add register) stores into register C the result of adding register A and register B.
addi (add immediate) stores into register C the result of adding register A and value B.

Multiplication:
mulr (multiply register) stores into register C the result of multiplying register A and register B.
muli (multiply immediate) stores into register C the result of multiplying register A and value B.

Bitwise AND:
banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.

Bitwise OR:
borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.

Assignment:
setr (set register) copies the contents of register A into register C. (Input B is ignored.)
seti (set immediate) stores value A into register C. (Input B is ignored.)

Greater-than testing:
gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.

Equality testing:
eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
"""
def set_val(a, b):
    return a

def r_op(regs, src1, src2, dst, func):
    out = [i for i in regs]
    out[dst] = int(func(regs[src1], regs[src2]))
    return out
def i_op(regs, src1, src2, dst, func):
    out = [i for i in regs]
    out[dst] = int(func(regs[src1], src2))
    return out
def i_op_rev(regs, src1, src2, dst, func):
    out = [i for i in regs]
    out[dst] = int(func(src1, regs[src2]))
    return out


def addr(regs, src1, src2, dst):
    return r_op(regs, src1, src2, dst, int.__add__)
def addi(regs, src1, src2, dst):
    return i_op(regs, src1, src2, dst, int.__add__)

def mulr(regs, src1, src2, dst):
    return r_op(regs, src1, src2, dst, int.__mul__)
def muli(regs, src1, src2, dst):
    return i_op(regs, src1, src2, dst, int.__mul__)

def banr(regs, src1, src2, dst):
    return r_op(regs, src1, src2, dst, int.__and__)
def bani(regs, src1, src2, dst):
    return i_op(regs, src1, src2, dst, int.__and__)

def borr(regs, src1, src2, dst):
    return r_op(regs, src1, src2, dst, int.__or__)
def bori(regs, src1, src2, dst):
    return i_op(regs, src1, src2, dst, int.__or__)

def setr(regs, src1, src2, dst):
    return r_op(regs, src1, src2, dst, set_val)
def seti(regs, src1, src2, dst):
    return i_op_rev(regs, src1, src2, dst, set_val)

def gtir(regs, src1, src2, dst):
    return i_op_rev(regs, src1, src2, dst, int.__gt__)
def gtri(regs, src1, src2, dst):
    return i_op(regs, src1, src2, dst, int.__gt__)
def gtrr(regs, src1, src2, dst):
    return r_op(regs, src1, src2, dst, int.__gt__)

def eqir(regs, src1, src2, dst):
    return i_op_rev(regs, src1, src2, dst, int.__eq__)
def eqri(regs, src1, src2, dst):
    return i_op(regs, src1, src2, dst, int.__eq__)
def eqrr(regs, src1, src2, dst):
    return r_op(regs, src1, src2, dst, int.__eq__)


operations = [addr, addi, mulr, muli,
              banr, bani, borr, bori,
              setr, seti, gtir, gtri,
              gtrr, eqir, eqri, eqrr]


def try_ops(regs, src1, src2, dst, op_no, op_dict={}):
    cnt = 0
    regs_in = regs[:4]
    regs_out = regs[4:]
    for o in operations:
        # print(o.__name__)
        # print('\tIns:', src1, src2, dst)
        # print('\tIn: ', regs_in)
        # print('\tOp: ', o(regs_in, src1, src2, dst))
        # print('\tOut:', regs_out)
        if op_no not in op_dict:
            op_dict[op_no] = {'maybe': set(), 'not': set()}
        if o(regs_in, src1, src2, dst) == regs_out:
            op_dict[op_no]['maybe'].add(o)
        else:
            op_dict[op_no]['not'].add(o)
            # print(o.__str__())
            cnt += 1
    # print('\tWorks like', cnt, 'ops')
    return cnt, op_dict


def match_op_codes(op_dict):
    found = set()
    aux = {}
    done = False
    guess_stack = []
    guessed = defaultdict(set)
    # while sum(len(aux[i]) for i in aux) > 16 or not done:
    while not done:
        # print(sum(len(aux[i]) for i in aux))
        changed = False
        # print('while')
        to_pop = []
        for op in op_dict:
            if op in aux:
                prev = aux[op]
            else:
                prev = None
            # What it could be minus what it couldn't be
            aux[op] = op_dict[op]['maybe'] & ((set(operations) - op_dict[op]['not']) - found)
            if prev != aux[op]:
                changed = True
            # Check for contradictions
            if len(aux[op]) == 0:
                aux, found, op_dict = guess_stack.pop(-1)
                break
            # print(op, len(aux[op]))
            # FOUND
            if len(aux[op]) == 1:
                found.add(a for a in aux[op])
                to_pop.append(op)
                # print('wow figured!', op)

        # Prune op_dict if solutions found
        [op_dict.pop(op, None) for op in to_pop]
        # Finished condition
        if sum(len(aux[i]) for i in aux) <= 16:
            done = True
            break

        # If it didn't changed we'll have to guess
        if not changed:
            print('Guess')
            guess_stack.append((aux, found, op_dict))

            # print('len', len(found), sorted(aux, key=lambda s: len(aux[s])), len(aux[3]))
            lowest = sorted(aux, key=lambda s: len(aux[s]))[len(found)]
            # print('lowest', lowest)
            available = [i for i in aux[lowest] if i not in guessed[lowest]]
            if len(available) == 0:
                print('Whoops, that should never happen!')
                raise Exception
            guessed[lowest].add(available[0])
            aux[lowest] = {available[0]}
            found.add(lowest)
            op_dict.pop(lowest)

    print('Correct configuration found:')
    # print(aux)
    # print(len(aux))
    for i in aux:
        aux[i] = aux[i].pop()
    return aux


def possible_operations_a(src1, src2, dst, before, after):
    result = set()
    for operation in operations:
        op_result = operation(before, src1, src2, dst)
        if op_result == after:
            result.add(operation)
    return result

def possible_operations(instruction, before, after):
    result = set()
    for operation in operations:
        op_result = operation(before, *instruction[1:])
        if op_result == after:
            result.add(operation)
    return result


def solve_a():
    with open('input.txt', 'r') as f:
        experiments = map(lambda s: list(map(int, re.findall(r'\d+', s))), f.read().split('\n\n\n\n')[0].split('\n\n'))

    cnt_3 = 0
    for nums in experiments:
        # nums = list([*i])
        regs = nums[0:4] + nums[8:12]
        op = nums[4]
        src1 = nums[5]
        src2 = nums[6]
        dst = nums[7]
        poss = possible_operations_a(src1, src2, dst, regs[0:4], regs[4:8])
        if len(poss) >= 3:
            cnt_3 += 1
    print('a:', cnt_3)
    # return len([experiment for experiment in experiments if len(possible_operations(*experiment)) >= 3])
    


def solve_b():
    # with open('input.txt', 'r') as f:
    #     read = f.read().split('\n\n\n\n')
    #     examples = list(map(lambda s: list(map(int, re.findall(r'\d+', s))), read[0].split('\n\n')))
    #     instructions = list(map(lambda s: map(int, re.findall(r'\d+', s)), read[1].strip().split('\n')))
    # 
    # op_dict = {}

    # [print(list(i)) for i in instructions]
    cnt_3 = 0
    # for c, i in enumerate(examples):
    #     # print(c)
    #     nums = list([*i])
    #     regs = nums[0:4] + nums[8:12]
    #     op = nums[4]
    #     src1 = nums[5]
    #     src2 = nums[6]
    #     dst = nums[7]
    #     _, op_dict = try_ops(regs, src1, src2, dst, op)
    # print('a:', cnt_3)
    # print(op_dict)
    # print(op_dict[14]['maybe'] & (set(operations) - op_dict[14]['not']))
    # op_dict = match_op_codes(op_dict)
    # for nums in experiments:
    #     print(nums)
    #     # nums = list([*experiment])
    #     opcode = nums[4]
    #     regs = nums[0:4] + nums[8:12]
    #     src1 = nums[5]
    #     src2 = nums[6]
    #     dst = nums[7]
    #     opers[opcode].intersection_update(possible_operations(src1, src2, dst, regs[0:4], regs[8:12]))
    
    # print(op_dict)
    # regs = [0, 0, 0, 0]
    # a = True
    # for op, src1, src2, dst in instructions:
    #     # if a:
    #     #     print(op, src1, src2, dst, op_dict[op])
    #     #     print(op, src1, src2, dst, op_dict[op].__name__)
    #     #     a = False
    #     # # print(op, src1, src2, dst)
    #     # print(regs)
    #     regs = op_dict[op](regs, src1, src2, dst)

    s = open('input.txt').read()
    if s and s[-1] == '\n':
        s = s[:-1]
    LINES = s.splitlines()
    experiments = []
    i = 0
    while LINES[i].strip():
        before, instruction, after = LINES[i:i + 3]
        i += 4
        experiments.append((
            list_map(int, instruction.split(' ')),
            eval(before[8:]),
            eval(after[8:])
        ))
    opers = {opcode: set(operations) for opcode in range(16)}
    for experiment in experiments:
        # print(experiment)
        opcode = experiment[0][0]
        opers[opcode].intersection_update(possible_operations(*experiment))

    while True:
        unique_ops = {}
        for op, ops in opers.items():
            if len(ops) == 1:
                unique_ops[op] = ops
        for op_, ops_ in unique_ops.items():
            for op, ops in opers.items():
                if op != op_:
                    ops.difference_update(ops_)
        if len(unique_ops) == len(opers):
            break

    for op in opers:
        opers[op] = opers[op].pop()

    registers = [0, 0, 0, 0]
    for line in LINES[i:]:
        if not line.strip():
            continue
        opcode, a, b, c = list_map(int, line.split(' '))
        registers = opers[opcode](registers, a, b, c)
    print(registers[0])


def ex():
    with open('inex.txt', 'r') as f:
        i = map(int, re.findall(r'\d+', f.read()))

    cnt_3 = 0
    nums = list(i)
    # print(nums)
    regs = nums[0:4] + nums[8:12]
    regs_in = regs[:4]
    regs_out = regs[4:]
    op = nums[4]
    src1 = nums[5]
    src2 = nums[6]
    dst = nums[7]
    if try_ops(regs, src1, src2, dst) >= 3:
        cnt_3 += 1
    print(cnt_3)


if __name__ == '__main__':
    # ex()
    solve_b()
    # print(type({1, 5, 7}))
    # print({1, 5, 7} - {1, 5})
