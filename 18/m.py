from typing import Any
from dataclasses import dataclass, field

from collections import Counter
import copy
import heapq
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
        # Newlines are part of the maze


def get_actions(maze, start_position, keys=tuple()):

    visited = set()
    actions = {}

    to_visit = queue.Queue()
    to_visit.put((start_position, 0))

    while not to_visit.empty():
        position, distance = to_visit.get()
        visited.add(position)

        value = maze[position]

        if (value in string.ascii_uppercase or value == "#") and value.lower() not in keys:
            continue

        if value in string.ascii_lowercase and value not in keys:
            actions[value] = distance
            continue

        for direction in DIRECTIONS:
            candidate = position + direction
            if candidate not in visited:
                to_visit.put((candidate, distance + 1))

    return actions


@dataclass(order=True)
class ExplorationState:
    dist: int
    keys: Any=field(compare=False)
    pos: Any=field(compare=False)


def shortest_path(maze, inverse, position):

    heap = []
    initial_state = ExplorationState(0, [], position)
    heapq.heappush(heap, initial_state)

    while True:
        state = heapq.heappop(heap)

        possible_actions = get_actions(maze, state.pos, state.keys)

        if len(possible_actions) == 0:
            print(state.keys)
            return state.dist

        for key, dist in possible_actions.items():
            next_state = ExplorationState(dist + state.dist, state.keys + [key], inverse[key])
            heapq.heappush(heap, next_state)


def part1():
    maze = get_maze(open("test2").readlines())
    inverse_maze = dict(map(reversed, maze.items()))
    start_point = inverse_maze["@"]
    return shortest_path(maze, inverse_maze, start_point)


print(part1())
