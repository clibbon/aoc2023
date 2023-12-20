import numpy as np


def read_input(path):
    with open(path, "r", encoding="utf-8") as f:
        entries = f.readlines()
    return entries


def parse(entry):
    """Parse something that looks like 
    Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    into (card_id, set(winners), set(numbers))"""
    card_id, number_section = [section.strip() for section in entry.split(":")]
    winning_number_section, selected_number_section = number_section.split("|")
    winners = set([int(number) for number in winning_number_section.split()])
    selected = set([int(number) for number in selected_number_section.split()])
    return card_id, winners, selected


def task_1():
    cards = read_input("input.txt")

    total = 0
    for card in cards:
        card_id, winners, selected = parse(card)
        n_winners = len(winners.intersection(selected))
        if n_winners >= 1:
            total += 2**(n_winners - 1)
    
    print(f"Total score is {total}")


def get_n_winners(card):
    _, winners, selected = parse(card)
    n_winners = len(winners.intersection(selected))
    return n_winners


def task_2():
    cards = read_input("input.txt")
    n_winners_per_card = [get_n_winners(card) for card in cards]
    result = np.ones(shape=(len(n_winners_per_card,)))

    for i, n_winners in enumerate(n_winners_per_card):
        if n_winners > 0:
            n_cards = result[i]
            result[i+1:i+n_winners+1] += n_cards
    
    total_cards = np.sum(result)
    print(f"Total cards won is {total_cards:.0f}")


if __name__ == "__main__":
    task_1()
    task_2()
