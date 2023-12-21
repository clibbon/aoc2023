import re
import sys


def in_map_range(input, mapping):
    in_lower_bound = input >= mapping[1]
    in_upper_bound = input <= mapping[1] + mapping[2] - 1
    return in_lower_bound & in_upper_bound


def get_adjustment(mapping):
    return mapping[0] - mapping[1]


def mapper_maker(mappings: list):
    """Generates functions that perform mappings"""
    adjustments = [get_adjustment(mapping) for mapping in mappings]
    
    def map(input):
        """Maps an input value to an outpungst value"""
        for mapping, adjustment in zip(mappings, adjustments):
            if in_map_range(input, mapping):
                return input + adjustment
        return input
    return map


def parse_input(filename):
    with open(filename, "r") as f:
        seeds_input = f.readline().strip()
        f.readline()

        mapping_functions = []
        
        for map in ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water",
                    "water-to-light", "light-to-temperature", "temperature-to-humidity",
                    "humidity-to-location"]:
            assert map in f.readline().strip()

            mappings = []
            while True:
                mapping_text = f.readline().strip()
                if mapping_text == "":
                    break
                mappings.append([int(number.strip()) for number in mapping_text.split()])
            # print(map, mappings)
            mapping_functions.append(mapper_maker(mappings))

        return seeds_input, mapping_functions


def task_1():
    seeds_input, mapping_functions = parse_input("input.txt")
    seed_ids = [int(seed_id) for seed_id in re.findall("(\\d+)", seeds_input)]

    min_location_seen = None

    for seed_id in seed_ids:
        value = seed_id
        for mapping_function in mapping_functions:
            value = mapping_function(value)

        if min_location_seen is None:
            min_location_seen = value
        elif value < min_location_seen:
            min_location_seen = value

    print(f"Minimum location seen {min_location_seen}")


def parse_input_task_2(filename):
    with open(filename, "r") as f:
        seeds_input = f.readline().strip()
        f.readline()

        all_mappings = []
        
        for map in ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water",
                    "water-to-light", "light-to-temperature", "temperature-to-humidity",
                    "humidity-to-location"]:
            assert map in f.readline().strip()

            mappings = []
            while True:
                mapping_text = f.readline().strip()
                if mapping_text == "":
                    break
                mappings.append([int(number.strip()) for number in mapping_text.split()])
            # print(map, mappings)
            all_mappings.append(mappings)

        return seeds_input, all_mappings


def process_mapping(mapping):
    """Turn mappings as provided into a continuous full range. For example:
    [50, 98, 2], [52, 50, 48]
    becomes:
    [(0, 49, 0), (50, 97, 2), (98, 99, -48), (100, 9223372036854775807, 0)]
    """
    sorted_mappings = sorted(mapping, key=lambda x: x[1])
    
    processed_mappings = []
    
    c_idx = 0
    start_of_first_mapping = sorted_mappings[0][1]
    # Handle direct mapping
    if start_of_first_mapping != 0:
        processed_mappings.append((0, start_of_first_mapping - 1, 0))
        c_idx = start_of_first_mapping
    
    # Handle declared mappings
    for mapping in sorted_mappings:
        start_of_mapping = mapping[1]
        end_of_mapping = start_of_mapping + mapping[2] - 1
        if c_idx < start_of_mapping:
            processed_mappings.append((c_idx, start_of_mapping - 1, 0))  # add a direct map
        processed_mappings.append((start_of_mapping, end_of_mapping, get_adjustment(mapping)))
        c_idx = end_of_mapping + 1
    
    processed_mappings.append((c_idx, sys.maxsize, 0))

    return processed_mappings


def calc_output_ranges(input_range, processed_mappings):
    """Given a range and a set of continuous mappings, find the output maps"""
    c_min = input_range[0]
    output_mappings = []
    
    for mapping in processed_mappings:
        if c_min > mapping[1]:
            continue
        output_range_start = max(mapping[0], c_min)
    
        if mapping[1] >= input_range[1]:
            output_range_end = input_range[1]
            output_mappings.append((output_range_start + mapping[2], output_range_end + mapping[2]))
            break
        else:
            output_range_end = mapping[1]
            output_mappings.append((output_range_start + mapping[2], output_range_end + mapping[2]))
            c_min = output_range_end + 1
            
    return output_mappings


def merge_ranges(ranges):
    merged_mappings = []

    sorted_outputs = sorted(ranges)
    current_range = None
    
    for mapping_range in sorted_outputs:
        if current_range is None:
            current_range = mapping_range
        elif (current_range[1] + 1) == mapping_range[0]:
            current_range = (current_range[0], mapping_range[1])
        else:
            merged_mappings.append(current_range)
            current_range = mapping_range
    
    merged_mappings.append(current_range)
    
    return merged_mappings


def task_2():
    seeds_input, all_mappings = parse_input_task_2("input.txt")
    seed_ids = [(int(seed_id[0]), int(seed_id[1])) for seed_id in re.findall("(\\d+) (\\d+)", seeds_input)]
    seed_ranges = [(ids[0], ids[0] + ids[1] - 1) for ids in sorted(seed_ids)]

    for mapping in all_mappings:
        processed_mapping = process_mapping(mapping)

        output_ranges = []
        for input_range in seed_ranges:
            output_ranges.extend(calc_output_ranges(input_range, processed_mapping))

        seed_ranges = merge_ranges(output_ranges)

    print(f"Task2 - Minimum location seen {min(output_ranges)[0]}")


if __name__ == "__main__":
    task_1()
    task_2()
