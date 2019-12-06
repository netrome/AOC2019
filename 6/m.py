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

print("P1: " + str(sum(map(len, map(all_orbits_for, parents)))))


# Part 2

def get_parent_line(child):
    line = set()
    parent = parents[child]

    while parent != "COM":
        line.add(parent)
        parent = parents[parent]

    return line


p1 = get_parent_line("YOU")
p2 = get_parent_line("SAN")


print(len(p1) + len(p2) - 2 * len(p1.intersection(p2)))


