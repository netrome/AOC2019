import re

inp = open("in").read()

def solve(s):
    program = list(map(int, re.findall(r"\d+", s)))

    program[1] = 12
    program[2] = 2

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

#print(solve("1,1,1,4,99,5,6,0,99"))
print(solve(inp))

