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
    cards = read_input("test_input.txt")

    total = 0
    for card in cards:
        card_id, winners, selected = parse(card)
        


if __name__ == "__main__":
    task_1()
