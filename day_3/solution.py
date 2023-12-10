import string
import numpy as np


SYMBOLS = "".join([symbol for symbol in string.punctuation if symbol != "."])


def sum_numbers(np_input, is_symbol):
    n_rows, n_columns = np_input.shape

    total = 0

    for i in range(n_rows):
        number_finished = False
        start_index = None
        end_index = None

        current_number = ''
        
        for j in range(n_columns):
            end_of_row = j == (n_columns - 1)
            
            if np_input[i, j] in string.digits:
                
                if start_index is None:
                    start_index = (max(0, i-1), max(0, j-1))
                    
                current_number += np_input[i, j]
                
            elif (current_number != '') and (np_input[i, j] not in string.digits):
                number_finished = True
            
            number_on_rhs = (end_of_row and current_number != '')
            
            if (number_on_rhs or number_finished):
                # the +1 +2 difference is because we moved on in the row and check if the current index is not a digit
                end_index = (min(i+2, n_rows), min(j+1, n_columns))
                print("number finished", current_number, start_index, end_index)

                number_valid = np.any(is_symbol[
                    start_index[0]:end_index[0],
                    start_index[1]:end_index[1]
                ])
                
                if number_valid:
                    total += int(current_number)
                
                current_number = ''
                start_index = None
                end_index = None
                number_finished = False
            
    return total


def parse_input(path):
    with open(path, "r", encoding="utf-8") as f:
        diagram = f.read().strip()
    np_input = np.array([[c for c in row] for row in diagram.split("\n")])
    is_symbol = np.array([[c in SYMBOLS for c in row] for row in diagram.split("\n")])
    return np_input, is_symbol


def task_1():
    np_input, is_symbol = parse_input("input.txt")
    total = sum_numbers(np_input, is_symbol)
    print(f"Total is {total}")


def find_leftmost_digit(start_idx, gear_array):
    """Keep going left until you either hit the edge or something that isn't a digit"""
    c_idx = np.copy(start_idx)
    while c_idx[1] > 0:
        if gear_array[c_idx[0], c_idx[1] - 1] in string.digits:
            c_idx[1] -= 1
        else:
            break
    return c_idx


def find_rightmost_digit(start_idx, gear_array):
    c_idx = np.copy(start_idx)
    n_columns = gear_array.shape[1]
    while c_idx[1] < (n_columns - 1):
        if gear_array[c_idx[0], c_idx[1] + 1] in string.digits:
            c_idx[1] += 1
        else:
            break
    return c_idx
    

def check_row_for_numbers(row, start_col, end_col, gear_array):
    current_col = start_col
    numbers_found = []
    
    while current_col <= end_col:
        if gear_array[row, current_col] in string.digits:
            left_most = find_leftmost_digit((row, current_col), gear_array)
            right_most = find_rightmost_digit((row, current_col), gear_array)

            number_str = gear_array[left_most[0],left_most[1]:right_most[1] + 1].tolist()
            number = int("".join(number_str))
            numbers_found.append(number)
            
            current_col = right_most[1] + 1
        else:
            current_col += 1
    return numbers_found  


def check_idx(idx, gear_array):
    n_rows, n_columns = gear_array.shape
    
    numbers_found = []
    
    # Check above
    if idx[0] > 0:
        numbers_found.extend(
            check_row_for_numbers(idx[0] - 1, max(0, idx[1] - 1), min(n_columns - 1, idx[1] + 1), gear_array)
        )
    # Check below
    if idx[0] < (n_rows - 1):
        numbers_found.extend(
            check_row_for_numbers(idx[0] + 1, max(0, idx[1] - 1), min(n_columns - 1, idx[1] + 1), gear_array)
        )

    # Check left
    if idx[1] > 0:
        if gear_array[idx[0], idx[1] - 1] in string.digits:
            left_most = find_leftmost_digit((idx[0], idx[1] - 1), gear_array)
            
            number_str = gear_array[left_most[0],left_most[1]:idx[1]].tolist()
            number = int("".join(number_str))
            numbers_found.append(number)
            
    # Check right
    if idx[1] < (n_columns - 1):
        if gear_array[idx[0], idx[1] + 1] in string.digits:
            right_most = find_rightmost_digit((idx[0], idx[1] + 1), gear_array)
            
            number_str = gear_array[right_most[0],idx[1] + 1: right_most[1] + 1].tolist()
            number = int("".join(number_str))
            numbers_found.append(number)
    
    return numbers_found


def task_2():
    np_input, _ = parse_input("input.txt")
    asterisks = np.argwhere(np_input == "*")
    total = 0

    for asterisk in asterisks:
        numbers = check_idx(asterisk, np_input)
        if len(numbers) == 2:
            total += numbers[0] * numbers[1]

    print(f"Total prodcut of gears is {total}")


if __name__ == "__main__":
    task_1()
    task_2()
