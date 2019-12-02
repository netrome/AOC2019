import re

inp = open("in").read()

def solve(noun, verb, s):
    program = list(map(int, re.findall(r"\d+", s)))

    program[1] = noun
    program[2] = verb

    def op(instr):
        operation = program[instr]
        if operation == 99:
            return "halt", None

        argp1, argp2, outp = program[instr + 1], program[instr + 2], program[instr + 3]

        if operation == 1:
            program[outp] = program[argp1] + program[argp2]
        elif operation == 2:
            program[outp] = program[argp1] * program[argp2]
        else:
            print("Error")
            return "error", None

        return "continue", instr + 4

    status = "continue"

    instr = 0

    while status == "continue":
        #print(program)
        status, instr = op(instr)

    return program[0]


for i in range(100):
    for j in range(100):
        solution = solve(i, j, inp)
        if solution == 19690720:
            print("Wihoo")
            print(100 * i + j)

