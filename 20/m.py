from collections import defaultdict
from dataclasses import dataclass

import string


DIRECTIONS = (-1, 1, -1j, 1j)


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

    start = portals["AA"]
    finish = portals["ZZ"]

    return Maze(grid, dict(portals), reverse_portals, start, finish)


def part1():
    l = open("in").readlines()
    maze = get_maze(l)


part1()
