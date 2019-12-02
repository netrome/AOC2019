import re


def add(memory, inptr):
    argp1, argp2, outp  = memory[inptr + 1], memory[inptr + 2], memory[inptr + 3]
    memory[outp] = memory[argp1] + memory[argp2]
    return "ok", inptr + 4


def multiply(memory, inptr):
    argp1, argp2, outp  = memory[inptr + 1], memory[inptr + 2], memory[inptr + 3]
    memory[outp] = memory[argp1] * memory[argp2]
    return "ok", inptr + 4


def halt(memory, inptr):
    return "halt", None


def compute(program, verb=None, noun=None):
    opcodes = {
        1: add,
        2: multiply,
        99: halt,
    }

    memory = list(map(int, program.split(",")))
    memory[1] = verb
    memory[2] = noun

    inptr = 0
    status = "ok"

    while status == "ok":
        instruction = memory[inptr]
        status, inptr = opcodes[instruction](memory, inptr)

    return memory[0]


def main():
    program = open("in").read()
    print(f"Part 1: {compute(program, 12, 2)}")

    for i in range(100):
        for j in range(100):
            val = compute(program, i, j)
            if val == 19690720:
                print(f"Part 2: {100 * i + j}")


if __name__ == "__main__":
    main()

