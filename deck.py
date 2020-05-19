import random

import numpy as np


class Card:

    def __init__(self, type, value):
        assert(value < 4)
        self.type = type
        self.value = value

    def value(self):
        return self.value

    def type(self):
        return self.type


class Deck:

    def __init__(self, ncards):
        assert(ncards % 4 == 0)
        self.cards = list()

        for i in range(int(ncards/4)):
            for value in range(4):
                self.cards.append(Card(i, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def cut(self, parts):
        return np.array_split(self.cards, parts)
