from collections import defaultdict
import itertools as it
import re
import threading
import queue


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


def jump_if_true(memory, inptr, pmodes):
    arg1, arg2 = _getparam(memory, inptr + 1, pmodes[0]), _getparam(memory, inptr + 2, pmodes[1])
    if arg1 != 0:
        return "ok", arg2
    return "ok", inptr + 3


def jump_if_false(memory, inptr, pmodes):
    arg1, arg2 = _getparam(memory, inptr + 1, pmodes[0]), _getparam(memory, inptr + 2, pmodes[1])
    if arg1 == 0:
        return "ok", arg2
    return "ok", inptr + 3


def less_than(memory, inptr, pmodes):
    arg1, arg2, outp  = _getparam(memory, inptr + 1, pmodes[0]), _getparam(memory, inptr + 2, pmodes[1]), memory[inptr + 3]
    if arg1 < arg2:
        memory[outp] = 1
    else:
        memory[outp] = 0
    return "ok", inptr + 4


def equals(memory, inptr, pmodes):
    arg1, arg2, outp  = _getparam(memory, inptr + 1, pmodes[0]), _getparam(memory, inptr + 2, pmodes[1]), memory[inptr + 3]
    if arg1 == arg2:
        memory[outp] = 1
    else:
        memory[outp] = 0
    return "ok", inptr + 4


def geninput(stream: queue.Queue):
    def inputop(memory, inptr, pmodes):
        outp  = memory[inptr + 1]
        memory[outp] = stream.get()
        return "ok", inptr + 2
    return inputop


def genoutput(stream: queue.Queue):
    def outputop(memory, inptr, pmodes):
        outp  = _getparam(memory, inptr + 1, pmodes[0])
        stream.put(outp)
        return "ok", inptr + 2
    return outputop


def halt(memory, inptr, pmodes):
    return "halt", None


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

    return "Ok"


def run_sequence_fn(program):
    def run_sequence(phase_settings):
        first_istream = queue.Queue()
        istream = first_istream
        ostream = queue.Queue()
        istream.put(phase_settings[0])
        istream.put(0)

        threads = []

        threads.append(threading.Thread(target=compute, args=(program, istream, ostream)))

        for phase_setting in phase_settings[1:-1]:
            istream = ostream
            ostream = queue.Queue()
            istream.put(phase_setting)
            threads.append(threading.Thread(target=compute, args=(program, istream, ostream)))

        istream = ostream
        ostream = first_istream
        istream.put(phase_settings[-1])
        threads.append(threading.Thread(target=compute, args=(program, istream, ostream)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return ostream.get()
    return run_sequence


def main():
    program = open("in").read()
    
    print(f"Debug: {run_sequence_fn(program)([9, 8, 7, 6, 5])}")

    ans = max(map(run_sequence_fn(program), it.permutations(range(5, 10))))
    print(ans)

if __name__ == "__main__":
    main()

