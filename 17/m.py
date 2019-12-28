from collections import defaultdict, Counter
import itertools as it

import intcomp

directions = (1, 0 + 1j, -1, 0 - 1j)

rotations = {
    "R": 1j,
    "L": -1j,
}


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


def get_path(scaffolds):
    point = 32 + 0j
    rot = "R"
    direction = 1

    commands = ["R"]

    acc = 0
    while True:
        next_point = point + direction

        if scaffolds[next_point] == 1:
            point = next_point
            acc += 1
            continue

        commands.append(str(acc))
        acc = 0

        rotated = False
        for rot in rotations:
            new_direction = direction * rotations[rot]
            next_point = point + new_direction
            if scaffolds[next_point] == 1:
                direction = new_direction
                commands.append(rot)
                rotated = True

        if not rotated:
            break
    return ",".join(commands)


def part1():
    program = open("in").read().strip()
    computer = intcomp.Computer()
    computer.run(program)

    codes = tuple(computer.join())
    #view_scaffolds(codes)
    s = scaffolds(codes)
    return sum(alignment_parameters(s))


def get_path_for_part2():
    program = open("in").read().strip()
    computer = intcomp.Computer()
    computer.run(program)

    codes = tuple(computer.join())
    s = scaffolds(codes)
    view_scaffolds(codes)
    return get_path(s)


def n_grams(n, seq):
    iterators = [iter(seq) for i in range(n)]
    for offset, i in enumerate(iterators):
        for j in range(offset):
            next(i)
    return zip(*iterators)


def repeating_subsequences(seq):
    subseqs = {}

    for n in range(2, 11):
        doku = Counter(n_grams(n, seq))

        for subseq, val in doku.items():
            subseqs[subseq] = n * val

    return tuple(reversed(sorted(map(tuple, map(reversed, subseqs.items())))))


print(f"Part 1: {part1()}")
seq = get_path_for_part2().split(",")
subseqs = repeating_subsequences(seq)
print(",".join(seq))
for val, sub in subseqs:
    print(",".join(sub))
