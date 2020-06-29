import random

import brain
import deck


class Player:
    '''
    The player class should manage the "real" aspects of being a player.
    This should primarily entail holding cards,
        taking turns, and telling the announcer things.
    Most of the logical inferences should be done by the Brain.
    The distributing of knowledge should be done through the Announcer,
        who will tell each player the new info.
    '''

    def __init__(self, cards, nkinds, id=0, strategy =0):
        self.cards = cards.tolist()
        self.opponents = list()
        self.nkinds = int(nkinds)
        self.id = id
        self.score = 0
        self.brain = brain.Brain(id, self.cards[:], self.nkinds)
        self.strategy = strategy

    # In order for a player to interact with opponents
    #   it needs access to their instance
    def intro_opponents(self, opponents):
        self.opponents.extend(opponents)
        for opponent in opponents:
            self.brain.intro_opponent(opponent.id)

    # Call this function to hand the turn to this player
    # The player will keep taking turns until it fails.
    def play(self):
        if self.strategy == 0 or 1:
            if self.certain_request():
			    # Clear all full sets
                self.removeKinds(self.brain.checkAllKinds())

			    # TODO: Inference based on counting cards
                self.perform_inference()


			    # Don't allow another turn if the game is over
                if self.brain.get_valid_kinds() != []:
                    self.play()
            else:
                return False
        if self.strategy == 2 or 3:
            if self.random_request():
			    # Clear all full sets
                self.removeKinds(self.brain.checkAllKinds())

			    # TODO: Inference based on counting cards
                self.perform_inference()
			    # Don't allow another turn if the game is over
                if self.brain.get_valid_kinds() != []:
                    self.play()
            else:
                return False
			
    def perform_inference(self):
        for kinds in self.brain.get_owned_kinds():
            kindSet = [deck.Card(kinds, value) for value in range(4)]
            ownSet = []
            for card in kindSet:
                if card in self.cards:
                    kindSet.remove(card)
                    
            for card in kindSet:
                total_sum = 0
                for player in self.opponents:
                    total_sum += self.brain.certain_cards(player.id, card)
                    #self.brain.certain_cards(player.id, card)
                            
                possible_card_owners = []
                if total_sum is 0:
                    for player in self.opponents:
                        if self.brain.certain_not_cards(player.id, card) is 0:
                            unknown_cards = self.brain.known_cards_number[player.id] - self.brain.get_number_of_requestable_cards(player.id)
                            if unknown_cards > 0:
                                possible_card_owners.append(player.id)
                    if len(possible_card_owners) is 1:
                        self.brain.add_card_to_knowledge(possible_card_owners, card)
                        print("I think player " + str(possible_card_owners) +  " has card number")
                        print(card)

    # This is the greedy strategy
    def certain_request(self):
        requestable_cards = self.brain.get_requestable_cards()
        if requestable_cards == []:
            return self.random_request()
        for opponent in self.opponents:
            if opponent.id == requestable_cards[0][1]:
                r = opponent.draw(requestable_cards[0][0])
                assert(r)
                self.cards.append(r)
                self.announcer.card_taken(r, opponent.id, self.id)
                return True
        return False

    # Request a random card of a valid kind from a random opponent
    def random_request(self):
        requestable_kinds = self.brain.get_owned_kinds()
        if requestable_kinds == []:
            return False
        kind = random.choice(requestable_kinds)
        hcard = deck.Card(kind, random.randrange(4))
        opponent = self.opponents[random.randrange(len(self.opponents))]
        r = opponent.draw(hcard)
        if not r:
            self.announcer.failed_request(hcard, opponent.id, self.id)
            return False
        else:
            self.cards.append(r)
            self.announcer.card_taken(r, opponent.id, self.id)
            return True

    # This function can be called by other players when they steal a card.
    # This function will return the taken card
    #   and will remove the card from the player's hand.
    def draw(self, card):
        try:
            self.cards.remove(card)
            return card
        except ValueError:
            return False

    # Take the cards from this kind out of the player's hand
    # Grant the player 1 point
    # Tells the announcer that this kind was removed
    def removeKinds(self, kinds):
        for kind in kinds:
            self.score += 1
            for val in range(4):
                card = deck.Card(kind, val)
                self.cards.remove(card)
            self.announcer.announce_remove_kind(kind, self.id)

    def __str__(self):
        return "P:" + str(self.id) + ", c:" + str(self.cards) + ", scr:" + str(self.score)

    # Give the player the instantiated announcer so they can announce things
    def set_announcer(self, announcer):
        self.announcer = announcer
