from collections import defaultdict


def solve(inp):
    wires = tuple(map(lambda i: i.split(","), inp.split("\n")))[:-1]

    directions = {
        "U": 1j,
        "R": 1,
        "D": -1j,
        "L": -1,
    }

    grid = defaultdict(lambda: defaultdict(int))

    def add_wire(origin, distance, command, tag):
        direction = directions[command[0]]
        length = int(command[1:])

        for i in range(1, length + 1):
            point = origin + i * direction
            grid[point][tag] = distance + i

        return origin + length * direction, distance + length

    for idx, wire in enumerate(wires):
        origin, distance = 0j, 0
        for command in wire:
            origin, distance = add_wire(origin, distance, command, idx)

    distances = tuple(map(lambda t: t[1][0] + t[1][1], filter(lambda t: len(t[1]) > 1, grid.items())))
    print(distances)

    return(sorted(distances)[0])

def main():
    inp = open("in").read()
    print(solve(inp))


main()
