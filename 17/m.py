from collections import defaultdict

import intcomp

directions = (1, 0 + 1j, -1, 0 - 1j)


def scaffolds(codes):
    u = defaultdict(int)
    pos = 0+0j

    for code in codes:
        if code != 46:
            u[pos] = 1
        if code == 10:
            pos = 0 + (pos.imag + 1) * 1j
        else:
            pos += 1
    return u


def view_scaffolds(codes):
    for code in codes:
        if code == 10:
            print()
        else:
            print(chr(code), end="")


def alignment_parameters(scaffolds):
    def is_intersection(pos):
        if not scaffolds[pos]:
            return False
        for direction in directions:
            if not scaffolds[pos + direction]:
                return False
        return True

    keys = tuple(scaffolds.keys())
    intersections = tuple(filter(is_intersection, keys))
    return tuple(map(lambda t: t.real * t.imag, intersections))


def part1():
    program = open("in").read().strip()
    computer = intcomp.Computer()
    computer.run(program)

    codes = tuple(computer.join())
    view_scaffolds(codes)
    s = scaffolds(codes)
    return sum(alignment_parameters(s))

print(f"Part 1: {part1()}")
