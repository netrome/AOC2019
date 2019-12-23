import copy
import numpy as np
import re


def parse_line(line):
    return tuple(map(int, re.findall(r"(-?\d+)", line)))


def get_gravity(position, positions):
    part1 = (position - positions) < 0
    part2 = (position - positions) > 0
    return (part1.astype(int) - part2.astype(int)).sum()


def gravity(positions):
    return np.array(list(map(lambda x: get_gravity(x, positions), positions)), dtype=int)


def step(x, dx):
    dx += gravity(x)
    x += dx


def fast_forward(x, dx, n=4096):
    g = gravity(x)
    first_order = tuple(np.argsort(x))

    x2 = x + n*dx + n*(n-1)*g
    dx2 = dx + n*g

    final_order = tuple(np.argsort(x2))

    if final_order == first_order or n == 1:
        return x2, dx2, n

    return fast_forward(x, dx, n/2)



def part1(lines, steps):
    positions = np.array(tuple(map(parse_line, lines)), dtype=int)
    velocities = positions * 0

    x, y, z = map(lambda i: positions[:, i], range(3))
    dx, dy, dz = map(lambda i: velocities[:, i], range(3))

    for i in range(steps):
        step(x, dx)
        step(y, dy)
        step(z, dz)

    return (np.abs(np.array([x, y, z])).sum(0) * np.abs(np.array([dx, dy, dz])).sum(0)).sum()


def period(x, dx, initial_x):
    for i in range(1, 1000_000):
        step(x, dx)

        x_state = tuple([*x, *dx])

        if x_state == initial_x:
            return i


def argmin(t):
    return sorted(zip(t, range(3)))[0][1]


def solve(px, py, pz):
    initial_periods = (px, py, pz)

    periods = list(initial_periods)

    while not (periods[0] == periods[1] == periods[2]):
        idx = argmin(periods)
        periods[idx] += initial_periods[idx]

    return periods[0]


def part2(lines):
    positions = np.array(tuple(map(parse_line, lines)), dtype=int)
    velocities = positions * 0

    x, y, z = map(lambda i: positions[:, i], range(3))
    dx, dy, dz = map(lambda i: velocities[:, i], range(3))

    initial_x = tuple([*x, *dx])
    initial_y = tuple([*y, *dy])
    initial_z = tuple([*z, *dz])

    print("Finding px")
    px = period(x, dx, initial_x)
    print("Finding py")
    py = period(y, dy, initial_y)
    print("Finding pz")
    pz = period(z, dz, initial_z)

    print(f"{[px, py, pz]}")

    return solve(px, py, pz)


ans = part1(open("in", "r").readlines(), 1000)
print(f"Part1: {ans}")


ans2 = part2(open("in", "r").readlines())
print(f"Part2: {ans2}")
