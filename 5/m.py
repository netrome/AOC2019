from collections import defaultdict
import re


def _getparam(memory, idx, mode):
    if mode == 0: # Position mode
        return memory[memory[idx]]
    return memory[idx] # Immediate mode


def add(memory, inptr, pmodes):
    arg1, arg2, outp  = _getparam(memory, inptr + 1, pmodes[0]), _getparam(memory, inptr + 2, pmodes[1]), memory[inptr + 3]
    memory[outp] = arg1 + arg2
    return "ok", inptr + 4


def multiply(memory, inptr, pmodes):
    arg1, arg2, outp  = _getparam(memory, inptr + 1, pmodes[0]), _getparam(memory, inptr + 2, pmodes[1]), memory[inptr + 3]
    memory[outp] = arg1 * arg2
    return "ok", inptr + 4


def geninput(stream):
    def inputop(memory, inptr, pmodes):
        outp  = memory[inptr + 1]
        memory[outp] = stream.pop()
        return "ok", inptr + 2
    return inputop


def genoutput(stream):
    def outputop(memory, inptr, pmodes):
        outp  = _getparam(memory, inptr + 1, pmodes[0])
        stream.append(outp)
        return "ok", inptr + 2
    return outputop


def halt(memory, inptr, pmodes):
    return "halt", None


def compute(program):
    istream = [1]
    ostream = []
    opcodes = {
        1: add,
        2: multiply,
        3: geninput(istream),
        4: genoutput(ostream),
        99: halt,
    }

    memory = list(map(int, program.split(",")))

    inptr = 0
    status = "ok"

    while status == "ok":
        instr_meta = list(map(int, str(memory[inptr])))
        pmodes = defaultdict(int)

        instruction = instr_meta.pop()

        try:
            second_digit = instr_meta.pop()
            instruction += second_digit * 10
        except IndexError:
            pass

        for pos, mode in enumerate(reversed(instr_meta)):
            pmodes[pos] = mode

        status, inptr = opcodes[instruction](memory, inptr, pmodes)

    return ostream


def main():
    program = open("in").read()
    print(f"Part 1: {compute(program)}")

if __name__ == "__main__":
    main()

