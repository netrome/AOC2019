from collections import defaultdict
import itertools as it
import time

import intcomp


tiles = {
    0: " ",
    1: "#",
    2: "¤",
    3: "^",
    4: "o",
}

incodes = {
    "a": -1,
    "s": 0,
    "d": 1,
    "": 0,
}


def parse_tile(t):
    pos = t[0] + t[1] * 1j
    return pos, t[2]


def render(universe):
    score = universe[-1]
    print(f"Score: {score}")
    max_x = int(max(map(lambda i: i.real, universe)))
    max_y = int(max(map(lambda i: i.imag, universe)))

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(tiles[universe[x + y * 1j]], end="")
        print()


def get_universe(tiles):
    universe = defaultdict(int)
    universe.update(map(parse_tile, zip(*([iter(tiles)] * 3))))
    return universe


def part1():
    program = open("in").read().strip()
    computer = intcomp.Computer()
    computer.run(program)
    tiles = computer.join()

    universe = get_universe(tiles)

    render(universe)

    return len(list(filter(lambda i: i==2, universe.values())))


def part2():
    program = open("in").read().strip()
    program = "2," + program[2:]
    computer = intcomp.Computer()
    computer.run(program)

    universe = defaultdict(int)

    while True:
        if not computer.process.is_alive():
            break

        time.sleep(0.01)
        tiles = computer.get_all()

        universe.update(get_universe(tiles))
        render(universe)

        inp = input("Next move")
        if len(inp) > 0:
            computer.input(incodes[inp[0]])
        else:
            computer.input(0)


    return len(list(filter(lambda i: i==2, universe.values())))


print(f"Part 1: {part1()}")
part2()
