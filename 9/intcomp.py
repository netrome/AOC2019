from collections import defaultdict
import queue


def _getparam(memory, idx, mode, relative_base):
    if mode == 0: # Position mode
        return memory[memory[idx]]
    if mode == 2:
        return memory[memory[idx] + relative_base]
    return memory[idx] # Immediate mode


def add(memory, inptr, pmodes, relative_base):
    arg1, arg2, outp  = _getparam(memory, inptr + 1, pmodes[0], relative_base), _getparam(memory, inptr + 2, pmodes[1], relative_base), memory[inptr + 3]

    if pmodes[2] == 2:
        outp += relative_base

    memory[outp] = arg1 + arg2
    return "ok", inptr + 4, relative_base


def multiply(memory, inptr, pmodes, relative_base):
    arg1, arg2, outp  = _getparam(memory, inptr + 1, pmodes[0], relative_base), _getparam(memory, inptr + 2, pmodes[1], relative_base), memory[inptr + 3]

    if pmodes[2] == 2:
        outp += relative_base

    memory[outp] = arg1 * arg2
    return "ok", inptr + 4, relative_base


def jump_if_true(memory, inptr, pmodes, relative_base):
    arg1, arg2 = _getparam(memory, inptr + 1, pmodes[0], relative_base), _getparam(memory, inptr + 2, pmodes[1], relative_base)
    if arg1 != 0:
        return "ok", arg2, relative_base
    return "ok", inptr + 3, relative_base


def jump_if_false(memory, inptr, pmodes, relative_base):
    arg1, arg2 = _getparam(memory, inptr + 1, pmodes[0], relative_base), _getparam(memory, inptr + 2, pmodes[1], relative_base)
    if arg1 == 0:
        return "ok", arg2, relative_base
    return "ok", inptr + 3, relative_base


def less_than(memory, inptr, pmodes, relative_base):
    arg1, arg2, outp  = _getparam(memory, inptr + 1, pmodes[0], relative_base), _getparam(memory, inptr + 2, pmodes[1], relative_base), memory[inptr + 3]

    if pmodes[2] == 2:
        outp += relative_base

    if arg1 < arg2:
        memory[outp] = 1
    else:
        memory[outp] = 0
    return "ok", inptr + 4, relative_base


def equals(memory, inptr, pmodes, relative_base):
    arg1, arg2, outp  = _getparam(memory, inptr + 1, pmodes[0], relative_base), _getparam(memory, inptr + 2, pmodes[1], relative_base), memory[inptr + 3]

    if pmodes[2] == 2:
        outp += relative_base

    if arg1 == arg2:
        memory[outp] = 1
    else:
        memory[outp] = 0
    return "ok", inptr + 4, relative_base


def adjust_relative_base(memory, inptr, pmodes, relative_base):
    arg  = _getparam(memory, inptr + 1, pmodes[0], relative_base)
    return "ok", inptr + 2, relative_base + arg


def geninput(stream: queue.Queue):
    def inputop(memory, inptr, pmodes, relative_base):
        outp  = memory[inptr + 1]
        if pmodes[0] == 2:
            outp += relative_base
        memory[outp] = stream.get()
        return "ok", inptr + 2, relative_base
    return inputop


def genoutput(stream: queue.Queue):
    def outputop(memory, inptr, pmodes, relative_base):
        outp  = _getparam(memory, inptr + 1, pmodes[0], relative_base)
        stream.put(outp)
        return "ok", inptr + 2, relative_base
    return outputop


def halt(memory, inptr, pmodes, relative_base):
    return "halt", None, relative_base


def compute(program, istream: queue.Queue, ostream: queue.Queue):
    opcodes = {
        1: add,
        2: multiply,
        3: geninput(istream),
        4: genoutput(ostream),
        5: jump_if_true,
        6: jump_if_false,
        7: less_than,
        8: equals,
        9: adjust_relative_base,
        99: halt,
    }

    memory = list(map(int, program.split(","))) + [0 for _ in range(10_000)]

    relative_base = 0
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

        status, inptr, relative_base = opcodes[instruction](memory, inptr, pmodes, relative_base)

    return "Ok"


def drain(queue):
    while not queue.empty():
        yield queue.get()


class Computer:
    def __init__(self):
        self.istream = queue.Queue()
        self.ostream = queue.Queue()

        self.process = None

    def input(self, num: int):
        self.istream.put(num)

    def run(self, program):
        self.process = threading.Thread(lambda: compute(program, self.istream, self.ostream))
        self.process.run()

    def join(self):
        self.process.join()
        return tuple(drain(self.ostream))

