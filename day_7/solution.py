from collections import Counter
import functools


RANKINGS = {"A": 0,
            "K": 1,
            "Q": 2,
            "J": 3,
            "T": 4}
for i in range(2, 10):
    RANKINGS[str(i)] = 14 - i
    

@functools.total_ordering
class Hand:
    def __init__(self, hand_string):
        self.hand = hand_string
        self.counts = Counter(hand_string).most_common()
        
    def __eq__(self, other):
        return self.hand == other.hand

    def __gt__(self, other):
        self_rank = self.get_rank()
        other_rank = other.get_rank()

        if self_rank > other_rank:
            return True
        elif other_rank > self_rank:
            return False
        else:
            return self.compare_highest_card(other)

    def __repr__(self):
        return self.hand

    def is_five_of_kind(self):
        return len(self.counts) == 1

    def is_four_of_kind(self):
        return self.counts[0][1] == 4

    def is_full_house(self):
        if len(self.counts) == 1:
            return False
        return (self.counts[0][1] == 3) and (self.counts[1][1] == 2)

    def is_three_of_kind(self):
        if len(self.counts) == 1:
            return False
        return (self.counts[0][1] == 3) and (self.counts[1][1] == 1)

    def is_two_pair(self):
        if len(self.counts) < 3:
            return False
        return (self.counts[0][1] == 2) and (self.counts[1][1] == 2)

    def is_pair(self):
        return len(self.counts) == 4

    def get_rank(self):
        if self.is_five_of_kind():
            return 6
        elif self.is_four_of_kind():
            return 5
        elif self.is_full_house():
            return 4
        elif self.is_three_of_kind():
            return 3
        elif self.is_two_pair():
            return 2
        elif self.is_pair():
            return 1
        else:
            return 0

    def compare_highest_card(self, other):
        for self_card, other_card in zip(self.hand, other.hand):
            if self_card == other_card:
                continue
            return RANKINGS[self_card] < RANKINGS[other_card]


def parse(filename):
    with open(filename, "r") as f:
        return f.readlines()


def task_1():
    lines = parse("input.txt")

    hands = []
    for line in lines:
        hand_string, bid = line.strip().split()
        hands.append((Hand(hand_string), int(bid)))

    total = 0
    for rank, hand in enumerate(sorted(hands)):
        total += (rank+1) * hand[1]
    
    print(f"Total score is {total}")


def count_w_jokers(hand_string):
    counts = Counter(hand_string)

    if ("J" in counts):
        all_jokers = len(counts) == 1
        if not all_jokers:
            n_to_add = counts.pop("J")
        else:
            print("All Jokers")
            n_to_add = 0
    else:
        n_to_add = 0

    highest = counts.most_common()
    if n_to_add > 0:
        most_common = highest[0]
        highest[0] = (most_common[0], most_common[1] + n_to_add)
    return highest
        

RANKING_WITH_JOKER = RANKINGS.copy()
RANKING_WITH_JOKER["J"] = 100


class HandWithJokers(Hand):
    
    def __init__(self, hand_string):
        self.hand = hand_string
        self.counts = count_w_jokers(hand_string)

    def compare_highest_card(self, other):
        for self_card, other_card in zip(self.hand, other.hand):
            if self_card == other_card:
                continue
            return RANKING_WITH_JOKER[self_card] < RANKING_WITH_JOKER[other_card]


def task_2():
    lines = parse("input.txt")

    hands = []
    for line in lines:
        if line.strip() == "":
            continue
        hand_string, bid = line.strip().split()
        try:
            hands.append((HandWithJokers(hand_string), int(bid)))
        except:
            print(hand_string)

    total = 0
    for rank, hand in enumerate(sorted(hands)):
        total += (rank+1) * hand[1]
    
    print(f"Total score is {total}")


if __name__ == "__main__":
    task_1()
    task_2()
