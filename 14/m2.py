import functools

from collections import defaultdict

import copy
import queue
import re


def parse_source(s):
    quantity = int(re.findall("\d+", s)[0])
    name = re.findall("\w+", s)[1]
    return name, quantity


def parse_reactions(line):
    sources, target = line.split("=>")
    sources = sources.split(",")

    sources = tuple(map(parse_source, sources))
    target = parse_source(target)

    return target[0], {"quantity": target[1], "sources": dict(sources)}


def reactands(reactions):
    reactands = defaultdict(set)
    for target in reactions:
        for source in reactions[target]["sources"]:
            reactands[source].add(target)
    return dict(reactands)



def distances(reactands):
    distances = {"ORE": 0}

    to_expand = queue.Queue()
    to_expand.put(("ORE", 0))

    while not to_expand.empty():
        element, distance = to_expand.get()
        children = reactands[element]

        for child in children:
            distances[child] = distance + 1

            if child != "FUEL":
                to_expand.put((child, distance + 1))

    return distances


def expand(reactions, targets, key):
    required_quantity = dict(targets)[key]
    min_unit = reactions[key]["quantity"]

    num_reactions = (required_quantity - 1) // min_unit + 1

    new_targets = defaultdict(int)
    new_targets.update(targets)
    del new_targets[key]

    for source, value in reactions[key]["sources"].items():
        new_targets[source] += value * num_reactions

    return frozenset(new_targets.items())


def gen_find_ore(reactions, distances):

    def find_ore(targets):
        sorted_targets = sorted(targets, key=lambda target: -distances[target[0]])

        if sorted_targets[0][0] == "ORE":
            return sorted_targets[0][1]

        new_targets = expand(reactions, targets, sorted_targets[0][0])

        return find_ore(new_targets)

    return find_ore


def part1():
    lines = open("in", "r").readlines()

    reactions = dict(map(parse_reactions, lines))
    dists = distances(reactands(reactions))

    targets = frozenset({("FUEL", 1)})

    find_ore = gen_find_ore(reactions, dists)

    return find_ore(targets)


def part2():
    lines = open("in", "r").readlines()

    reactions = dict(map(parse_reactions, lines))
    dists = distances(reactands(reactions))
    find_ore = gen_find_ore(reactions, dists)

    max_ore = 1000000000000

    approx_ore_per_fuel = find_ore(frozenset({("FUEL", 1)}))

    fuel_guess = max_ore // approx_ore_per_fuel
    total_ore = find_ore(frozenset({("FUEL", fuel_guess)}))

    for i in range(100):
        delta = max_ore - total_ore

        step = delta // approx_ore_per_fuel

        fuel_guess += step
        total_ore = find_ore(frozenset({("FUEL", fuel_guess)}))

    return fuel_guess


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
