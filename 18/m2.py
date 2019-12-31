import itertools as it
import queue
import string


DIRECTIONS = {1, 1j, -1, -1j}


def get_maze(lines):
    maze = {}

    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            # The newlines will not be harmful today
            maze[x + y * 1j] = val

    return maze


def view_maze(maze):
    max_x = int(max(map(lambda i: i.real, maze)))
    max_y = int(max(map(lambda i: i.imag, maze)))

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(maze[x + y * 1j], end="")


def inverse(maze):
    return dict(map(reversed, maze.items()))


def get_keys(inverse_maze):
    return set(filter(lambda k: k in string.ascii_lowercase, inverse_maze.keys())).union({"@"})


def distance_and_doors(maze, p1, p2):
    """ Returns distances and doors between two arbitrary points in the maze """

    visited = set()

    to_visit = queue.Queue()
    to_visit.put((p1, 0, set()))

    while not to_visit.empty():
        position, distance, doors = to_visit.get()

        if position == p2:
            return distance, doors

        visited.add(position)

        value = maze[position]

        if value in string.ascii_uppercase:
            doors = doors.union({value})

        if value == "#":
            continue

        for direction in DIRECTIONS:
            candidate = position + direction
            if candidate not in visited:
                to_visit.put((candidate, distance + 1, doors))


def distances_and_doors(maze):
    """ Returns the distances and doors between each pair of keys, including @ """
    inv = inverse(maze)
    all_keys = get_keys(inv)

    dnd = {}

    for k1, k2 in it.combinations(all_keys, 2):
        p1, p2 = inv[k1], inv[k2]
        x = distance_and_doors(maze, p1, p2)
        dnd[(k1, k2)] = x
        dnd[(k2, k1)] = x

    return dnd


def part1():
    maze = get_maze(open("test2").readlines())
    dnd = distances_and_doors(maze)
    print(dnd)


part1()
