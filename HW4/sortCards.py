"""
file: sortCards.py
description: CSCI-665.04 - HMWK4: Q3 - minimum number of cards that need to be moved to sort the list
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779
"""

def sortCards(cards: list):
    # initializing the DParray
    DParray = [1] * len(cards)
    for i in range(1, len(cards)):
        for j in range(i):
            # recurrence relation
            if cards[i] > cards[j] and DParray[i] < DParray[j] + 1:
                DParray[i] = 1 + DParray[j]
    # solution
    return len(cards) - max(DParray)


if __name__ == '__main__':
    # number of cards
    n = int(input())
    # list of cards
    cards = list(int(num) for num in input().strip().split())
    print(sortCards(cards))

