import itertools as it

inp = open("in").readlines()

parents = dict()

for parent, child in map(lambda i: i.split(")"), inp):
    parent, child = parent.strip(), child.strip()

    parents[child] = parent

def all_orbits_for(child):
    orbits = {(child, "COM")}
    ancestor = parents[child]

    while ancestor != "COM":
        orbits.add((child, ancestor))
        ancestor = parents[ancestor]

    return orbits

print(sum(map(len, map(all_orbits_for, parents))))
