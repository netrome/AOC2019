from collections import defaultdict
from dataclasses import dataclass

import queue
import string


DIRECTIONS = (-1, 1, -1j, 1j)

TORUS_DIVISOR = (18 + 18j, 101 + 101j)


@dataclass
class Maze:
    grid: dict
    portals: dict
    reverse_portals: dict
    start: complex
    finish: complex


def _get_grid(lines):
    grid = defaultdict(lambda: " ")
    for row, line in enumerate(lines):
        for col, token in enumerate(line):
            grid[row + col * 1j] = token
    return grid


def portal(point, grid):
    """ Returns the name of the portal if the point is a portal, else None """
    for direction in DIRECTIONS:
        if grid[point + direction] in string.ascii_uppercase:
            letters = [grid[point + direction], grid[point + direction * 2]]
            if direction in [-1, -1j]:
                return "".join(reversed(letters))
            return "".join(letters)

    return None


def get_maze(lines):
    grid = _get_grid(lines)
    portals = defaultdict(set)
    reverse_portals = {}

    open_spaces = map(lambda t: t[0], filter(lambda t: t[1] == ".", grid.items()))
    for point in open_spaces:
        maybe_portal = portal(point, grid)
        if maybe_portal:
            portals[maybe_portal].add(point)
            reverse_portals[point] = maybe_portal

    start = next(iter(portals["AA"]))
    finish = next(iter(portals["ZZ"]))

    return Maze(grid, dict(portals), reverse_portals, start, finish)


def _is_inner(point):
    return point.imag > TORUS_DIVISOR[0].imag and point.real > TORUS_DIVISOR[0].real and point.imag < TORUS_DIVISOR[1].imag and point.real < TORUS_DIVISOR[1].real


def possible_moves(point, maze, level=None):
    moves = set()

    for direction in DIRECTIONS:
        candidate = point + direction
        if maze.grid[candidate] == ".":
            if level is not None:
                moves.add((candidate, level))
            else:
                moves.add(candidate)

    if point in maze.reverse_portals:
        for candidate in maze.portals[maze.reverse_portals[point]]:
            if candidate != point:
                if level is not None:
                    next_level = level + 1 if _is_inner(point) else level - 1
                    moves.add((candidate, next_level))
                else:
                    moves.add(candidate)

    return moves


def shortest_path(start, finish, maze):
    to_visit = queue.Queue()
    to_visit.put((start, 0))
    seen = {start}

    while not to_visit.empty():
        point, dist = to_visit.get()

        if point == finish:
            return dist

        for next_point in filter(lambda p: p not in seen, possible_moves(point, maze)):
            to_visit.put((next_point, dist+1))
            seen.add(next_point)

    return None


def shortest_path_with_level(start, finish, maze):
    to_visit = queue.Queue()
    to_visit.put((start, 0, 0))
    seen = {start}

    while not to_visit.empty():
        point, level, dist = to_visit.get()

        if point == finish and level == 0:
            return dist

        for next_point, next_level in filter(lambda p: p not in seen and p[1] >= 0, possible_moves(point, maze, level)):
            to_visit.put((next_point, next_level, dist+1))
            seen.add((next_point, next_level))

    return None


def part1():
    l = open("in").readlines()
    maze = get_maze(l)

    return shortest_path(maze.start, maze.finish, maze)


def part2():
    l = open("in").readlines()
    maze = get_maze(l)

    return shortest_path_with_level(maze.start, maze.finish, maze)


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
