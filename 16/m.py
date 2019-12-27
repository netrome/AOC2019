import itertools as it
import math
import functools


def pattern(n):
    base_pattern = [0, 1, 0, -1]
    pattern = it.chain(*map(lambda i: it.repeat(i, n+1), base_pattern))
    pattern_iterator = it.cycle(pattern)
    next(pattern_iterator)
    return pattern_iterator


def pattern_at(n, i):
    shifted = i + 1
    n_plus_one = n + 1
    return round(math.sin( (shifted // n_plus_one % 4) * math.pi / 2))


def nth_fft_element(numbers, n):
    p = pattern(n)
    s = sum(map(lambda t: t[0] * t[1], zip(numbers, p)))
    return abs(s) % 10


def nth_fft_element_alt(numbers, n):
    s = sum(map(lambda t: t[1]*pattern_at(n, t[0]), enumerate(numbers)))
    return abs(s) % 10


def fft_phase(numbers):
    return tuple(map(functools.partial(nth_fft_element_alt, numbers), range(len(numbers))))


def backward_fft(numbers):
    """ Much faster than the forward one, yields the correct values for the latter half of the fft """
    def accumulate():
        s = 0
        for val in reversed(numbers):
            s += val
            yield s

    return tuple(reversed(tuple(map(lambda x: abs(x) % 10, accumulate()))))


def part1(digits):
    vals = tuple(map(int, str(digits)))

    for _ in range(100):
        vals = fft_phase(vals)

    return "".join(map(str, vals[:8]))


def part2(digits):
    vals = tuple(list(map(int, str(digits))) * 10_000)
    offset = int(str(digits)[:7])
    print(offset)

    for _ in range(100):
        vals = backward_fft(vals)

    return "".join(map(str, vals[offset:offset + 8]))

my_input = int(open("in").read().strip())
test0 = 12345678
test1 = 80871224585914546619083218645595
test2 = 19617804207202209144916044189917 

print(f"Part1 {part1(test1)}")

test3 = "03036732577212944063491565474664"
print(f"Part2 {part2(my_input)}")
