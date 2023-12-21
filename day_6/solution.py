import re
import math
import functools


def parse(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    times = [int(time) for time in re.findall("\\d+", lines[0])]
    distances = [int(distance) for distance in re.findall("\\d+", lines[1])]
    return times, distances


def calc_limits(T, d):
    quad = (T**2 - 4 * d)**.5
    lower_bound = math.ceil(math.nextafter((T - quad)/2, math.inf))
    upper_bound = math.floor(math.nextafter((T + quad)/2, -math.inf))
    return lower_bound, upper_bound


def get_n_ints(number_range):
    """Find the number of integer values in the number range (inclusive). 
    e.g. (2,5) -> 2, 3, 4, 5 = 4 values"""
    return number_range[1] - number_range[0] + 1


def task_1():
    times, distances = parse("input.txt")
    n_solutions = [get_n_ints(calc_limits(T, d)) for T, d in zip(times, distances)]
    total = functools.reduce(lambda x, y: x*y, n_solutions)
    
    print(f"Product of total possible solutions is {total}")


def parse_task_2(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    time = int(''.join(time for time in re.findall("\\d+", lines[0])))
    distance = int(''.join(distance for distance in re.findall("\\d+", lines[1])))
    return time, distance


def task_2():
    T, d = parse_task_2("input.txt")
    n_solutions = get_n_ints(calc_limits(T, d))
    
    print(f"Total possible solutions is {n_solutions}")


if __name__ == "__main__":
    task_1()
    task_2()
