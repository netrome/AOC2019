from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Maze:
    grid: dict
    portals: dict
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
    pass


def get_maze(lines):
    grid = _get_grid(lines)

    open_spaces = map(lambda t: t[0], filter(lambda t: t[1] == ".", grid.items()))
    for point in open_spaces:
        maybe_portal = portal(point, grid)


def part1():
    l = open("in").readlines()


part1()
