import queue

import intcomp


def run_boost(program) -> queue.Queue:
    computer = intcomp.Computer()
    computer.input(1)
    computer.run(program)
    return computer.join()


def main():
    program = open("in").read()
    
    print(run_boost(program))


if __name__ == "__main__":
    main()
