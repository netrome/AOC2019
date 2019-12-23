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


def super_smart_ai(universe):
    reverse_universe = dict(map(reversed, universe.items()))
    ball = reverse_universe[4]
    paddle = reverse_universe[3]

    diff = ball.real - paddle.real

    if diff > 0:
        return 1
    if diff < 0:
        return - 1
    return 0


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
    time.sleep(1)

    while True:
        if not computer.process.is_alive():
            break

        time.sleep(0.04)
        tiles = computer.get_all()

        universe.update(get_universe(tiles))
        render(universe)

        computer.input(super_smart_ai(universe))


    return len(list(filter(lambda i: i==2, universe.values())))


print(f"Part 1: {part1()}")
part2()
