import numpy as np


def parse_input(file_path):
    test_input = open(file_path).read().strip()
    return np.array([[c for c in line] for line in test_input.split("\n")])


def expand(parsed_input):
    columns_to_expand = np.argwhere(~np.all(parsed_input==".", axis=0))
    rows_to_expand = np.argwhere(~np.all(parsed_input==".", axis=1))

    new_rows = 2*parsed_input.shape[0] - rows_to_expand.shape[0]
    new_columns = 2*parsed_input.shape[1] - columns_to_expand.shape[0]

    print(f"Original shape = {parsed_input.shape}, new = {new_rows},{new_columns}")

    # Expand rows first
    expanded_rows = np.chararray(shape=(new_rows,parsed_input.shape[1]))
    expanded_rows[:] = "."

    offset = np.cumsum(np.concatenate([np.array([[0]]), np.diff(rows_to_expand, axis=0) - 1], axis=0))
    expanded_rows[rows_to_expand[:,0] + offset, :] = parsed_input[rows_to_expand[:,0],:]

    # Then expand the columns
    expanded = np.chararray(shape=(expanded_rows.shape[0],new_columns))
    expanded[:] = "."

    offset = np.cumsum(np.concatenate([np.array([[0]]), np.diff(columns_to_expand, axis=0) - 1], axis=0))
    expanded[:, columns_to_expand[:,0] + offset] = expanded_rows[:,columns_to_expand[:,0]]

    return expanded


def get_distance(galaxy_a, galaxy_b):
    return np.sum(np.abs(galaxy_a - galaxy_b))


def task_1():
    parsed_input = parse_input("input.txt")
    expanded = expand(parsed_input)

    galaxy_list = np.argwhere(expanded == b"#")
    print(f"Found {len(galaxy_list)} galaxies")

    total_distance = 0

    for i in range(len(galaxy_list)):
        for j in range(i+1,len(galaxy_list)):
            total_distance += get_distance(galaxy_list[i], galaxy_list[j])

    print(total_distance)


def expand_cunnigly(parsed_input, factor):
    columns_to_expand = np.argwhere(~np.all(parsed_input==".", axis=0))
    rows_to_expand = np.argwhere(~np.all(parsed_input==".", axis=1))

    unexpanded_locations = np.argwhere(parsed_input=="#")

    row_offset = np.cumsum(np.concatenate([np.array([[0]]), np.diff(rows_to_expand, axis=0) - 1], axis=0)) * (factor-1)
    col_offset = np.cumsum(np.concatenate([np.array([[0]]), np.diff(columns_to_expand, axis=0) - 1], axis=0)) * (factor-1)
    expanded_rows = rows_to_expand[:,0] + row_offset
    expanded_columns = columns_to_expand[:,0] + col_offset
    
    row_mapping = {orig: expanded for (orig, expanded) in zip(rows_to_expand[:,0], expanded_rows)}
    col_mapping = {orig: expanded for (orig, expanded) in zip(columns_to_expand[:,0], expanded_columns)}

    expanded_galaxy_list = []
    for i in range(unexpanded_locations.shape[0]):
        row, col = unexpanded_locations[i]
        
        expanded_galaxy_list.append((row_mapping[row], col_mapping[col]))

    return np.array(expanded_galaxy_list)


def task_2():
    parsed_input = parse_input("input.txt")
    galaxy_list = expand_cunnigly(parsed_input, factor=1e6)

    print(f"Found {len(galaxy_list)} galaxies")

    total_distance = 0

    for i in range(len(galaxy_list)):
        for j in range(i+1,len(galaxy_list)):
            total_distance += get_distance(galaxy_list[i], galaxy_list[j])

    print(total_distance)


if __name__ == "__main__":
    task_1()
    task_2()
