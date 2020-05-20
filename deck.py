import random

import numpy as np


class Card:
    '''
    A card has a Kind and a Value.
    The kind can be thought of as the group of 4 that a card falls in.
    The value can be thought of as an ID of where in that group the card is.
    '''

    def __init__(self, kind, value):
        assert(value < 4)
        self.kind = kind
        self.value = value

    def __str__(self):
        return "<" + str(self.kind) + "," + str(self.value) + ">"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if(self.value == other.value and
           self.kind == other.kind):
            return True
        else:
            return False


class Deck:
    '''
    A deck consists of any number of kinds, where each kind has 4 cards.
    The deck class can be used to instantiate,
        shuffle and distribute a set of cards.
    '''
    def __init__(self, ncards):
        assert(ncards % 4 == 0)
        self.cards = list()
        self.ncards = ncards
        self.nkinds = int(ncards / 4)
        for i in range(self.nkinds):
            for value in range(4):
                self.cards.append(Card(i, value))

    def shuffle(self):
        random.shuffle(self.cards)

    # Divide the deck into as-even-as possible sets
    # Returns a list of np arrays
    def cut(self, parts):
        return np.array_split(self.cards, parts)
