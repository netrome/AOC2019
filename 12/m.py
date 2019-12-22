import copy
import numpy as np
import re


def parse_line(line):
    return tuple(map(int, re.findall(r"(-?\d+)", line)))


def get_gravity(position, positions):
    part1 = (position - positions) < 0
    part2 = (position - positions) > 0
    return (part1.astype(int) - part2.astype(int)).sum(0)


def gravity(positions):
    return np.array(list(map(lambda x: get_gravity(x, positions), positions)), dtype=int)


def step(positions, velocities):
    velocities += gravity(positions)
    positions += velocities


def energy(positions, velocities):
    return np.sum(np.abs(positions).sum(1) * np.abs(velocities).sum(1))


def part1(lines, steps):
    positions = np.array(tuple(map(parse_line, lines)), dtype=int)
    velocities = positions * 0

    for i in range(steps):
        step(positions, velocities)

    return energy(positions, velocities)


ans = part1(open("in", "r").readlines(), 1000)
print(f"Part1: {ans}")
