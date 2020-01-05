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


def f_deal_to_new_stack(formula):
    return (formula[0] + 1) * (-1), formula[1] * (-1)


def f_cut(n, formula):
    return formula[0] - n, formula[1]


def f_deal_with_increment(n, formula):
    return formula[0] * n, formula[1] * n


def parse_technique(line):
    if "deal with inc" in line:
        val = int(re.findall("-?\d+", line)[0])
        return functools.partial(deal_with_increment, val)

    if "cut" in line:
        val = int(re.findall("-?\d+", line)[0])
        return functools.partial(cut, val)

    if "deal into new stack" in line:
        return deal_to_new_stack


def f_parse_technique(line):
    if "deal with inc" in line:
        val = int(re.findall("-?\d+", line)[0])
        return functools.partial(f_deal_with_increment, val)

    if "cut" in line:
        val = int(re.findall("-?\d+", line)[0])
        return functools.partial(f_cut, val)

    if "deal into new stack" in line:
        return f_deal_to_new_stack

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


def test21():
    deck = tuple(range(10))
    formula = 0, 1

    deck = parse_technique("deal with increment 7")(deck)
    formula = f_parse_technique("deal with increment 7")(formula)

    deck = parse_technique("deal with increment 9")(deck)
    formula = f_parse_technique("deal with increment 9")(formula)

    deck = parse_technique("cut -2")(deck)
    formula = f_parse_technique("cut -2")(formula)

    assert indexof(4, deck) == (formula[0] + formula[1] * 4) % 10


def test22():
    deck = tuple(range(10))
    formula = 0, 1

    deck = parse_technique("cut 6")(deck)
    formula = f_parse_technique("cut 6")(formula)

    deck = parse_technique("deal with increment 7")(deck)
    formula = f_parse_technique("deal with increment 7")(formula)

    deck = parse_technique("deal into new stack")(deck)
    formula = f_parse_technique("deal into new stack")(formula)


    assert indexof(4, deck) == (formula[0] + formula[1] * 4) % 10
    assert indexof(5, deck) == (formula[0] + formula[1] * 5) % 10
    assert indexof(6, deck) == (formula[0] + formula[1] * 6) % 10


def part1():
    instructions = open("in").readlines()

    deck = tuple(range(10007))

    for line in instructions:
        deck = parse_technique(line)(deck)

    return indexof(2019, deck)


def part2():
    instructions = open("in").readlines()

    size = 10007
    formula = 0, 1

    for line in instructions:
        formula = f_parse_technique(line)(formula)

    return (formula[0] + formula[1] * 2019) % size

test1()
test2()
test3()
print(f"Part 1: {part1()}")
test21()
test22()
print(f"Part 2: {part2()}")
