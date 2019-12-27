from collections import defaultdict
import queue

import intcomp


DIRECTIONS = {
    1: 0 + 1j,
    2: 0 - 1j,
    3: -1 - 0j,
    4: 1 - 0j
}


TILES = {
    0: "#",
    1: ".",
    2: "O",
}


def choose_step(payloads, explored_maze, position):
    return min(map(lambda t: (t[0], payloads[position + t[1]]), DIRECTIONS.items()), key=lambda t: t[1])[0]


def give_order(payloads, explored_maze, position, step, computer):
    step = choose_step(payloads, explored_maze, position)
    attempted_position = position + DIRECTIONS[step]
    payloads[attempted_position] += 1

    computer.input(step)
    response = computer.get()

    explored_maze[attempted_position] = response

    if response == 0:
        return position

    return attempted_position


def explore(computer):
    payloads = defaultdict(int)
    position = 0 + 0j
    explored_maze = {position: 1}

    for i in range(5000):
        step = choose_step(payloads, explored_maze, position)
        position = give_order(payloads, explored_maze, position, step, computer)

    return explored_maze


def fewest_commands(maze):
    q = queue.Queue()

    q.put((0 + 0j, 0))
    visited = set()

    while not q.empty():
        position, distance = q.get()
        visited.add(position)

        if maze[position] == 2:
            return distance

        for direction in DIRECTIONS.values():
            candidate_position = position + direction
            if candidate_position not in visited and maze[candidate_position] != 0:
                q.put((candidate_position, distance + 1))

    return 1337


# I should probably factor out this logic, since I do this so often...
def render(maze: dict):
    min_x = int(min(map(lambda i: i.real, maze)))
    max_x = int(max(map(lambda i: i.real, maze)))
    min_y = int(min(map(lambda i: i.imag, maze)))
    max_y = int(max(map(lambda i: i.imag, maze)))

    def tile(x, y):
        coord = x + y * 1j
        if coord not in maze:
            return " "
        return TILES[maze[coord]]

    def gen_tiles():
        for row in  range(max_y, min_y - 1, -1):
            for col in range(min_x, max_x + 1):
                if row == col == 0:
                    yield "X"
                else:
                    yield tile(col, row)
            yield "\n"

    return "".join(gen_tiles())


def part1():
    program = open("in", "r").read().strip()
    computer = intcomp.Computer()
    computer.run(program)

    maze = explore(computer)
    return fewest_commands(maze)


print(f"Part 1: {part1()}")

