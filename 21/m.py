import intcomp


def to_ascii(s):
    return tuple(map(ord, s))


def from_ascii(s):
    return "".join(map(chr, s))


def part1():
    script = """
NOT C J
AND D J
NOT A T
OR T J
WALK
""".strip()

    program = open("in").read().strip()
    computer = intcomp.Computer()
    computer.run(program)

    for c in to_ascii(script):
        computer.input(c)
    computer.input(10)

    out = computer.join()

    try:
        print(from_ascii(out))
    except Exception:
        print(from_ascii(out[:-1]))

    return out[-1]


def part2():
    script = """
NOT A J
NOT C T
AND D T
AND H T
OR T J
NOT B T
AND D T
AND H T
OR T J
OR D T
AND E T
OR T J
RUN
""".strip()

    program = open("in").read().strip()
    computer = intcomp.Computer()
    computer.run(program)

    for c in to_ascii(script):
        computer.input(c)
    computer.input(10)

    out = computer.join()

    try:
        print(from_ascii(out))
    except Exception:
        print(from_ascii(out[:-1]))

    return out[-1]


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
