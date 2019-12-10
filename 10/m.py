import functools

inp = open("in")

asteroid_positions = set()

for y, vals in enumerate(inp.readlines()):
    for x, val in enumerate(vals):
        if val == "#":
            asteroid_positions.add((x, y))

def get_angle(t1, t2):
    if t1 == t2:
        return 0
    diff = (t2[0] - t1[0], t2[1] - t1[1])
    if diff[0] == 0:
        return (0, diff[1]/abs(diff[1]))
    return (diff[0] / abs(diff[0]), diff[1] / abs(diff[0]))


def close_enough(t1, t2):
    diff = (t2[0] - t1[0], t2[1] - t1[1])
    if abs(diff[0]) + abs(diff[1]) < 1e-5:
        return True
    return False
    

def get_all_angles(t1, positions):
    return set(map(functools.partial(get_angle, t1), positions))


scores = tuple(map(lambda pos: (len(get_all_angles(pos, asteroid_positions)) - 1, pos), asteroid_positions))

print(sorted(scores))
