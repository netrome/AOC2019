from collections import defaultdict
from typing import Any
from dataclasses import dataclass, field

import heapq
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


def get_actions(key, all_keys, collected_keys, dnd):
    def is_ok(k):
        if k in collected_keys:
            return False
        doors = dnd[(key, k)][1]
        return all(map(lambda door: door.lower() in collected_keys or door.lower() not in all_keys, doors))

    def action(k):
        return dnd[(key, k)][0]

    return dict(map(lambda k: (k, action(k)), filter(is_ok, all_keys)))


@dataclass(order=True)
class ExplorationState:
    dist: int
    keys: Any=field(compare=False)
    key: Any=field(compare=False)

    def __hash__(self):
        return hash(frozenset(self.keys)) + hash(self.dist) + hash(self.key)


def shortest_path(dnd):
    all_keys = set(it.chain(*dnd)).union({"@"})
    heap = []
    collected_keys = ["@"]

    initial_state = ExplorationState(0, collected_keys, "@")

    visited = {initial_state}

    heapq.heappush(heap, initial_state)

    while True:
        state = heapq.heappop(heap)
        print(state.dist, end="\r")

        possible_actions = get_actions(state.key, all_keys, state.keys, dnd)

        if len(possible_actions) == 0:
            return state.dist, "".join(state.keys + [state.key])

        for key, dist in possible_actions.items():
            next_state = ExplorationState(dist + state.dist, state.keys + [key], key)
            if next_state not in visited:
                visited.add(next_state)
                heapq.heappush(heap, next_state)


def quadrant(c):
    re, im = c.real, c.imag
    if re != 0:
        renorm = re / abs(re)
    else:
        renorm = 0
    if im != 0:
        imnorm = im / abs(im)
    else:
        imnorm = 0
    return renorm + imnorm * 1j


def into_quadrants(dnd, pivot, maze):
    quadrants = defaultdict(dict)
    inv = inverse(maze)

    pivot = inv[pivot]

    for k1, k2 in dnd:
        p1, p2 = inv[k1], inv[k2]
        q1, q2 = quadrant(p1 - pivot), quadrant(p2 - pivot)
        if q1 == q2:
            quadrants[q1][(k1, k2)] = dnd[(k1, k2)]
        if q1 == 0:
            quadrants[q2][(k1, k2)] = dnd[(k1, k2)]
        if q2 == 0:
            quadrants[q1][(k1, k2)] = dnd[(k1, k2)]

    return quadrants



def part1():
    maze = get_maze(open("in").readlines())
    collected_keys = {"@"}
    print("Computing dnd...", end="\r")
    dnd = distances_and_doors(maze)
    print("                ", end="\r")
    #print(get_actions("@", all_keys, collected_keys, dnd))
    print(shortest_path(dnd))


def part2():
    maze = get_maze(open("in").readlines())

    pivot = inverse(maze)["@"]
    extras = "pqrs"
    for d, extra in zip(DIRECTIONS, extras):
        d2 = d * 1j
        maze[pivot + d + d2] = extra

    dnd = distances_and_doors(maze)
    quadrants = into_quadrants(dnd, "@", maze)

    s = 0
    for quadrant in quadrants.values():
        s += shortest_path(quadrant)[0]

    return s - 8


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
