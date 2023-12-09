from typing import List, Tuple
from functools import reduce


REFERENCE = {"red": 12,
             "green": 13,
             "blue": 14}


def parse_input(filename) -> List[Tuple[int, List]]:
    """Games look like Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green, need to parse this into:
    (5, [{red: 6, blue: 1, green: 3}, ....])"""
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    parsed_games = []

    for line in lines:
        id_section, games_section = line.strip().split(":")
        _, game_id_string = id_section.strip().split()
        game_id = int(game_id_string)

        games = [game.strip() for game in games_section.split(";")]
        game_dicts = []
        for game in games:
            color_entries = game.split(",")
            color_dict = {}
            for entry in color_entries:
                amount, color = entry.strip().split()
                color_dict[color] = int(amount)

            game_dicts.append(color_dict)

        parsed_games.append((game_id, game_dicts))
            
    return parsed_games


def get_max_seen(game_sets):
    """Given a list of game sets, find the max number of each color seen across all the sets."""
    running_max = {k: 0 for k in REFERENCE}
    for game_set in game_sets:
        for color, value in game_set.items():
            running_max[color] = max(running_max[color], value)
    return running_max


def is_possible(game, reference) -> bool:
    """Checks if a game is possible"""
    max_seen = get_max_seen(game[1])

    for color, reference_value in reference.items():
        if max_seen[color] > reference_value:
            return False
    return True


def get_power(game) -> int:
    max_seen = get_max_seen(game[1])
    power = reduce(lambda x, y: x * y, max_seen.values())
    return power


def task_1():
    games = parse_input("input.txt")
    possible_games = [game for game in games if is_possible(game, REFERENCE)]
    total = sum(game[0] for game in possible_games)
    print(f"Sum of all possible games is {total}")


def task_2():
    games = parse_input("input.txt")
    powers = [get_power(game) for game in games]
    print(f"Sum of power of all games is {sum(powers)}")


if __name__ == "__main__":
    task_1()
    task_2()
