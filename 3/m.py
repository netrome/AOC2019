from collections import defaultdict


def solve(inp):
    wires = tuple(map(lambda i: i.split(","), inp.split("\n")))[:-1]

    directions = {
        "U": 1j,
        "R": 1,
        "D": -1j,
        "L": -1,
    }

    grid = defaultdict(set)

    def add(origin, command, tag):
        direction = directions[command[0]]
        length = int(command[1:])

        for i in range(1, length + 1):
            point = origin + i * direction
            grid[point].add(tag)

        return origin + length * direction

    for idx, wire in enumerate(wires):
        origin = 0j
        for command in wire:
            origin = add(origin, command, idx)

    intersections = tuple(map(lambda t: t[0], filter(lambda t: len(t[1]) > 1, grid.items())))
    distances = tuple(map(lambda i: int(abs(i.real) + abs(i.imag)), intersections))


    return(sorted(distances)[0])

def main():
    inp = open("in").read()
    print(solve(inp))


main()
