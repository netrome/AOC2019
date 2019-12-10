import math
from collections import defaultdict
import numpy as np
import functools

inp = open("in")

asteroid_positions = set()

for y, vals in enumerate(inp.readlines()):
    for x, val in enumerate(vals):
        if val == "#":
            asteroid_positions.add((x, y))

def size(vec):
    return vec[0] ** 2 + vec[1] ** 2

def angle(vec):
    val = np.angle(-vec[1] + vec[0] * 1j)
    if val < 0:
        val += 2 * math.pi
    return val

def get_angle(t1, t2):
    if t1 == t2:
        return None
    diff = (t2[0] - t1[0], t2[1] - t1[1])
    return angle(diff)

def close_enough(t1, t2):
    diff = (t2[0] - t1[0], t2[1] - t1[1])
    if abs(diff[0]) + abs(diff[1]) < 1e-5:
        return True
    return False
    

def get_all_angles(t1, positions):
    return set(map(functools.partial(get_angle, t1), positions))


scores = tuple(map(lambda pos: (len(get_all_angles(pos, asteroid_positions)) - 1, pos), asteroid_positions))

num_asteroids, station = sorted(scores)[-1]

print(f"P1 ans: {num_asteroids}")

relative_positions = set(map(lambda pos: (pos[0] - station[0], pos[1] - station[1]), asteroid_positions - {station}))

all_asteroids = defaultdict(list)

for position in relative_positions:
    ang = angle(position)
    all_asteroids[ang].append(position)

for key in all_asteroids:
    all_asteroids[key] = sorted(all_asteroids[key], key=lambda i: -size(i))

num_popped = 0
ioi = None
while len(all_asteroids) > 0:
    keys = sorted(all_asteroids.keys())
    for key in keys:
        item = all_asteroids[key].pop()
        num_popped += 1
        if not all_asteroids[key]:
            del all_asteroids[key]
        if num_popped == 200:
            ioi = item

point = (ioi[0] + station[0], ioi[1] + station[1])

print(f"P2 ans: {point[0]*100 + point[1]}")
