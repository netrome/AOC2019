from collections import defaultdict
import intcomp


def get_grid(program, xr, yr):
    grid = defaultdict(int)
    for x in range(xr):
        for y in range(yr):
            computer = intcomp.Computer(memsize=30)
            computer.run(program)
            computer.input(x)
            computer.input(y)
            grid[x + y * 1j]  = computer.get()

    return grid


def efficient_grid_finder(program, xr, yr):
    grid = defaultdict(int)
    upper = 5
    lower = 5j

    while upper.real < xr and lower.real < yr:
        computer = intcomp.Computer(memsize=30)
        computer.run(program)
        computer.input(upper.real)
        computer.input(upper.imag)
        upper_val = computer.get()
        grid[upper] = upper_val

        if upper_val == 1:
            grid[upper + 1j] = 1
            upper += 1
        else:
            upper += 1j

        computer = intcomp.Computer(memsize=30)
        computer.run(program)
        computer.input(lower.real)
        computer.input(lower.imag)
        lower_val = computer.get()
        grid[lower] = lower_val

        if lower_val == 1:
            grid[lower + 1] = 1
            lower += 1j
        else:
            lower += 1

    return grid


def view_grid(grid, xr, yr):
    for x in range(xr):
        for y in range(yr):
            if y == x:
                print("#", end="")
            elif y == 2*x:
                print("#", end="")
            else:
                print(grid[x + y * 1j], end="")
        print()


def largest_square(point, grid, xr, yr):
    xsize, ysize = 0, 0

    pos = point + xsize
    passed = False
    for _ in range(200):
        pos = point + xsize
        xsize += 1

        if grid[pos] == 1:
            passed = True

        if passed and grid[pos] == 0:
            break

    pos = point + ysize * 1j
    passed = False
    for _ in range(200):
        pos = point + ysize * 1j
        ysize += 1

        if grid[pos] == 1:
            passed = True

        if passed and grid[pos] == 0:
            break

    return min(xsize, ysize) - 1, xsize > ysize


def find_squares(grid, xr, yr):
    point = 45 + 70j

    while True:
        size, c = largest_square(point, grid, 100, 100)
        if size == 100:
            return point
        if c:
            point += 1
        else:
            point += 1j

        if point.real > xr or point.imag > yr:
            return "Noooose"


def part1():
    program = open("in").read().strip()

    grid = get_grid(program, 50, 50)
    return sum(grid.values())


def part2():
    program = open("in").read().strip()

    grid = efficient_grid_finder(program, 1400, 1400)

    point = find_squares(grid, 1400, 1400)
    return point.real * 10000 + point.imag


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
