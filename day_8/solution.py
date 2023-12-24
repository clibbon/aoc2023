from itertools import cycle


def parse(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    lr_index_map = {"L": 0, "R": 1}

    instructions = [lr_index_map[c] for c in lines[0].strip()]

    nodes = {}

    for line in lines[2:]:
        start, mapping_string = line.strip().split(" = ")
        mapping = tuple(mapping_string[1:-1].split(", "))

        nodes[start] = mapping

    return instructions, nodes


def task_1():
    instructions, nodes = parse("input.txt")
    instruction_loop = cycle(instructions)

    current_node = "AAA"
    actions_limit = 100_000
    actions_taken = 0

    while current_node != "ZZZ":
        next_instruction = next(instruction_loop)
        current_node = nodes[current_node][next_instruction]

        actions_taken += 1
        if actions_taken > actions_limit:
            print("Action limit reached")
            break

    print(f"Took {actions_taken} actions")


def task_2():
    print("Task 2 was tough! See day_8_task_2.ipynb for solution")


if __name__ == "__main__":
    task_1()
    task_2()
