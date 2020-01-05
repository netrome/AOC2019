import functools
import re


def deal_to_new_stack(deck):
    return tuple(reversed(deck))


def cut(n, deck):
    return deck[n:] + deck[:n]


def deal_with_increment(n, deck):
    out = [0 for i in range(len(deck))]

    for idx, card in enumerate(deck):
        out[(idx * n) % len(deck)] = card

    return tuple(out)


def parse_technique(line):
    if "deal with inc" in line:
        val = int(re.findall("-?\d+", line)[0])
        return functools.partial(deal_with_increment, val)

    if "cut" in line:
        val = int(re.findall("-?\d+", line)[0])
        return functools.partial(cut, val)

    if "deal into new stack" in line:
        return deal_to_new_stack


def test1():
    deck = tuple(range(10))
    deck = parse_technique("deal with increment 7")(deck)
    deck = parse_technique("deal into new stack")(deck)
    deck = parse_technique("deal into new stack")(deck)
    assert deck == tuple(map(int, "0 3 6 9 2 5 8 1 4 7".split()))


def test2():
    deck = tuple(range(10))
    deck = parse_technique("cut 6")(deck)
    deck = parse_technique("deal with increment 7")(deck)
    deck = parse_technique("deal into new stack")(deck)
    assert deck == tuple(map(int, "3 0 7 4 1 8 5 2 9 6".split()))


def test3():
    deck = tuple(range(10))
    deck = parse_technique("deal with increment 7")(deck)
    deck = parse_technique("deal with increment 9")(deck)
    deck = parse_technique("cut -2")(deck)
    assert deck == tuple(map(int, "6 3 0 7 4 1 8 5 2 9".split()))


def indexof(card, deck):
    return tuple(map(lambda t: t[0], filter(lambda t: t[1]==card, enumerate(deck))))[0]


def part1():
    instructions = open("in").readlines()

    deck = tuple(range(10007))

    for line in instructions:
        deck = parse_technique(line)(deck)

    return indexof(2019, deck)

test1()
test2()
test3()
print(f"Part 1: {part1()}")
