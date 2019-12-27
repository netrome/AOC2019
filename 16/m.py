import itertools as it
import functools


def pattern(n):
    base_pattern = [0, 1, 0, -1]
    pattern = it.chain(*map(lambda i: it.repeat(i, n+1), base_pattern))
    pattern_iterator = it.cycle(pattern)
    next(pattern_iterator)
    return pattern_iterator


def nth_fft_element(numbers, n):
    p = pattern(n)
    s = sum(map(lambda t: t[0]*t[1], zip(numbers, p)))
    return abs(s) % 10


def fft_phase(numbers):
    return tuple(map(functools.partial(nth_fft_element, numbers), range(len(numbers))))


def part1(digit):
    vals = tuple(map(int, str(digit)))

    for _ in range(100):
        vals = fft_phase(vals)

    return "".join(map(str, vals[:8]))


def part2(digit):
    vals = tuple(it.repeat(map(int, str(digit)), 1000))
    print(vals)

my_input = int(open("in").read().strip())
test0 = 12345678
test1 = 80871224585914546619083218645595
test2 = 19617804207202209144916044189917 
print(f"Part1 {part1(my_input)}")


