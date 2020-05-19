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

    def __str__(self):
        return "<" + str(self.type) + "," + str(self.value) + ">"

    def __eq__(self, other):
        if(self.value == other.value and
           self.type == other.type):
            return True
        else:
            return False


class Deck:

    def __init__(self, ncards):
        assert(ncards % 4 == 0)
        self.cards = list()
        self.ncards = ncards
        for i in range(int(ncards/4)):
            for value in range(4):
                self.cards.append(Card(i, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def cut(self, parts):
        return np.array_split(self.cards, parts)

    def ntypes(self):
        return self.ncards / 4
