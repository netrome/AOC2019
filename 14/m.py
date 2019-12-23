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
    required_quantity = dict(targets)[key]
    min_unit = reactions[key]["quantity"]

    num_reactions = (required_quantity - 1) // min_unit + 1

    new_targets = defaultdict(int)
    new_targets.update(targets)
    del new_targets[key]

    for source, value in reactions[key]["sources"].items():
        new_targets[source] += value * num_reactions

    return frozenset(new_targets.items())


def gen_find_ore(reactions):
    @functools.lru_cache(100_000)
    def find_ore(targets):
        candidates = []
        for key, value in targets:
            if key != "ORE" and value > 0:
                new_targets = expand(reactions, targets, key)
                candidates.append(find_ore(new_targets))

        if len(candidates) == 0:
            return dict(targets)["ORE"]

        return min(candidates)
    return find_ore


def part1():
    lines = open("test3", "r").readlines()

    reactions = dict(map(parse_reactions, lines))
    find_ore = gen_find_ore(reactions)

    targets = frozenset({("FUEL", 1)})

    return find_ore(targets)


print(f"Part 1: {part1()}")
