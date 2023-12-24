import numpy as np


def parse(filename):
    with open(filename, "r", encoding="utf-8") as f:
        inputs = [
            np.array([int(e) for e in line.strip().split()]) for line in f.readlines()
        ]
    return inputs


def get_next_diff(list_in):
    """Recursively find next difference in a sequence."""
    diffs = np.diff(list_in)

    if np.any(diffs):
        return diffs[-1] + get_next_diff(diffs)
    else:
        return 0


def task_1():
    inputs = parse("input.txt")

    total = 0

    for _input in inputs:
        next_difference = get_next_diff(_input)
        next_in_seq = _input[-1] + next_difference
        total += next_in_seq

    print(f"Total of next terms per sequence is {total}")


def task_2():
    inputs = parse("input.txt")

    total = 0

    for _input in inputs:
        reversed_input = _input[::-1]
        next_difference = get_next_diff(reversed_input)
        next_in_seq = reversed_input[-1] + next_difference
        total += next_in_seq

    print(f"Total of previous terms per sequence is {total}")


if __name__ == "__main__":
    task_1()
    task_2()
