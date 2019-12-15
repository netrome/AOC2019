from collections import defaultdict
import intcomp


class Robot:

    def __init__(self, program):
        self.computer = intcomp.Computer()
        self.computer.run(program)

        self.hull = defaultdict(int)

        self.position = 0 + 0j

        self.direction = 1j

    def step(self):
        i = self.hull[self.position]
        self.computer.input(i)
        color, turn = self.computer.get(), self.computer.get()

        if isinstance(color, str):
            return "Done"

        self.hull[self.position] = color

        if turn == 0:
            self.turn_left()
        else:
            self.turn_right()

        self.position += self.direction

    def turn_left(self):
        self.direction *= 1j

    def turn_right(self):
        self.direction *= -1j


def display_hull(hull: dict):
    x = tuple(map(lambda i: int(i.real), hull))
    y = tuple(map(lambda i: int(i.imag), hull))

    def msg():
        for row in range(max(y), min(y)-1, -1):
            for col in range(min(x), max(x) + 1):
                val = row * 1j + col
                if val in hull:
                    if hull[val]:
                        yield "#"
                    else:
                        yield "."
                else:
                    yield " "
            yield "\n"

    print("".join(map(lambda i: i, msg())))


def part1():
    program = open("in").read().strip()
    robot = Robot(program)

    while robot.step() != "Done":
        pass

    print(f"Part 1: {len(robot.hull)}")


def part2():
    program = open("in").read().strip()
    robot = Robot(program)
    robot.hull[0 + 0j] = 1

    while robot.step() != "Done":
        pass

    display_hull(robot.hull)

    print(f"Part 2: {len(robot.hull)}")

if __name__ == "__main__":
    #part1()
    part2()
