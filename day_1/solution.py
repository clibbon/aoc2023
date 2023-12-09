"""Day 1 solution"""
import string
import re

PATTERN = re.compile(
    "(?=(one|two|three|four|five|six|seven|eight|nine|" + "|".join(string.digits) + "))"
)
REPLACEMENTS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def parse_input(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


def extract_value(calibration_line):
    digits = [c for c in calibration_line if c in string.digits]
    return int(digits[0] + digits[-1])


def extract_value_w_written(calibration_line):
    "Tricky as the first encountered should be translated."
    digits = PATTERN.findall(calibration_line)
    first_digit = REPLACEMENTS[digits[0]] if digits[0] in REPLACEMENTS else digits[0]
    last_digit = REPLACEMENTS[digits[-1]] if digits[-1] in REPLACEMENTS else digits[-1]
    return int(first_digit + last_digit)


def task_1():
    calibration_lines = parse_input("input.txt")
    calibration_values = [extract_value(line) for line in calibration_lines]
    total = sum(calibration_values)
    print(f"Sum of calibration values is {total}")


def task_2():
    calibration_lines = parse_input("input.txt")
    calibration_values = [extract_value_w_written(line) for line in calibration_lines]

    total = sum(calibration_values)
    print(f"Sum of the updated calibration values is {total}")


if __name__ == "__main__":
    task_1()
    task_2()
