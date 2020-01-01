from collections import defaultdict
import intcomp


def get_grid(program, xr, yr):
    grid = defaultdict(int)
    for x in range(xr):
        for y in range(yr):
            computer = intcomp.Computer(memsize=100)
            computer.run(program)
            computer.input(x)
            computer.input(y)
            grid[x + y * 1j]  = computer.get()

    return grid


def view_grid(grid, xr, yr):
    for x in range(xr):
        for y in range(yr):
            print(grid[x + y * 1j], end="")
        print()


def part1():
    program = open("in").read().strip()

    grid = get_grid(program, 50, 50)
    return sum(grid.values())


print(f"Part 1: {part1()}")
