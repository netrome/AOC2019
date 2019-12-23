import functools

from collections import defaultdict

import copy
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


def expand(reactions, targets, key):
    required_quantity = targets[key]
    min_unit = reactions[key]["quantity"]

    num_reactions = (required_quantity - 1) // min_unit + 1

    new_targets = copy.deepcopy(targets)

    new_targets[key] = 0
    for source, value in reactions[key]["sources"].items():
        new_targets[source] += value * num_reactions

    return new_targets


def find_ore(reactions, targets):
    candidates = []
    for key, value in targets.items():
        if key != "ORE" and value > 0:
            new_targets = expand(reactions, targets, key)
            candidates.append(find_ore(reactions, new_targets))

    if len(candidates) == 0:
        return targets["ORE"]

    return min(candidates)


def part1():
    lines = open("test2", "r").readlines()

    reactions = dict(map(parse_reactions, lines))

    targets = defaultdict(int)
    targets["FUEL"] = 1

    return find_ore(reactions, targets)


print(f"Part 1: {part1()}")
