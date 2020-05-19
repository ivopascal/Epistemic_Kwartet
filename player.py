import random

import deck


class Player:

    def __init__(self, cards, ntypes, id=0):
        self.cards = cards.tolist()
        self.opponents = list()
        self.ntypes = int(ntypes)
        self.id = id
        self.score = 0

    def intro_opponents(self, opponents):
        self.opponents.extend(opponents)

    def play(self):
        if self.random_request():
            self.play()
            self.checkAllSets()
            self.printCards()
        else:
            return False

    def random_request(self):
        hcard = deck.Card(random.randrange(self.ntypes),
                          random.randrange(4))
        r = self.opponents[
                random.randrange(len(self.opponents))].draw(
                hcard)
        if not r:
            return False
        else:
            self.cards.append(r)
            return True

    def draw(self, card):
        try:
            self.cards.remove(card)
            return card
        except ValueError:
            return False

    def printCards(self):
        print(str(self.id) + " has " + str(len(self.cards)))

    def checkSingleSet(self, set):
        for val in range(4):
            card = deck.Card(set, val)
            if card not in self.cards:
                return
        # Here we may announce a set is removed
        self.score += 1
        for val in range(4):
            card = deck.Card(set, val)
            self.cards.remove(card)

    def checkAllSets(self):
        for set in range(self.ntypes):
            self.checkSingleSet(set)

    def score(self):
        return self.score
