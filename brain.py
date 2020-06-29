import deck


class Known_player:
    '''
    The Known_player class is distinctly different from the Player class.
    A Known_player here is the representation of
        a participant that exists in the brain.
    You can therefore not interact with a Known_player,
    but you can store your knowledge about that player here.

    E.g. in this class I store that Known_player2 has card <8,3>,
            then I can ask Player2 for card <8,3>
    '''
    def __init__(self, id, certainCards=None, certainNotCards=None):
        self.id = id
        self.certainCards = list()
        self.certainNotCards = list()
        self.knownKinds = list()
        self.number_of_cards = 13

        if certainCards is not None:
            self.certainCards.extend(certainCards)
        if certainNotCards is not None:
            self.certainNotCards.extend(certainNotCards)

    # Removes all cards of this kind from the Known_player
    # After this it should be known that
    #    the Known_player does not hold any card of this kind
    def remove_kind(self, kind):
        kindSet = [deck.Card(kind, value) for value in range(4)]
        for card in self.certainCards:
            if card in kindSet:
                self.certainCards.remove(card)
                self.number_of_cards -=1

    def card_taken(self, card):
        self.exclude_card(card)
        self.number_of_cards -=1

    def card_given(self, card):
        if card not in self.certainCards:
            self.certainCards.append(card)
            self.number_of_cards +=1
        if card in self.certainNotCards:
            self.certainNotCards.remove(card)
        if card.kind not in self.knownKinds:
            self.knownKinds.append(card.kind)

    # Player cannot have card because it is somewhere else
    def exclude_card(self, card):
        if card in self.certainCards:
            self.certainCards.remove(card)
        if card not in self.certainNotCards:
            self.certainNotCards.append(card)
        if card.kind in self.knownKinds:
            self.knownKinds.remove(card.kind)
	
    def owns_card_of_type(self, card):
        self.knownKinds.append(card.kind)

class Brain:
    '''
    The Brain class is intended as the knowledge center of a player.
    Where the Player class handles the actions that a player may execute,
    the brain class holds the knowledge that a player may have.
    '''

    # Make sure to pass cards by value with [:]  !
    # If cards not passed by value mutations outside the brain
    # will also occur inside the brain.
    def __init__(self, id, cards, nkinds):
        self.known_players = list()
        self.known_cards_number = list()
        self.known_cards_number.append(13)
        self.known_cards_number.append(13)
        self.known_cards_number.append(13)
        self.known_cards_number.append(13)
        self.removed_kinds = list()
        self.nkinds = nkinds
        self.cards = cards
        self.id = id
        print(self.cards)

    # Let's the brain become aware that an opponent exists
    # This allows it to keep track of how many components there are
    def intro_opponent(self, id):
        self.known_players.append(Known_player(id, certainNotCards=self.cards))

    # Tells the brain that a Kind is removed from the game
    # This does not actually remove any cards,
    #    it only removes knowledge of cards
    def remove_kind(self, kind, id):
        self.removed_kinds.append(kind)
        if id == self.id:
            for value in range(4):
                self.cards.remove(deck.Card(kind, value))
        for known_player in self.known_players:
            known_player.remove_kind(kind)

    # Returns all Kinds that have not yet been removed from the game
    def get_valid_kinds(self):
        return list(set(range(self.nkinds)) - set(self.removed_kinds))

    # Check whether the player has a full set of a given Kind
    #   and remove it if he does
    def checkSingleKind(self, kind):
        for val in range(4):
            card = deck.Card(kind, val)
            if card not in self.cards:
                return
        return kind

    # Check all Kinds to see if the player has any full sets of any Kind
    def checkAllKinds(self):
        full_kinds = list()
        for kind in range(self.nkinds):
            r = self.checkSingleKind(kind)
            if r is not None:
                full_kinds.append(r)
        return full_kinds

    # Learn that a card was taken from giver
    # Determine who had that card and remove it from the mental model of them
    def card_taken(self, card, giver):
        if giver == self.id:
            self.cards.remove(card)
        else:
            for known_player in self.known_players:
                if known_player.id == giver:
                    known_player.card_taken(card)
                else:
                    known_player.exclude_card(card)


    # Learn that a card was given to a player
    # Determine the player who received the card and add the card to the mental
    # model of them.
    def card_given(self, card, receiver):
        if receiver == self.id:
            self.cards.append(card)
        else:
            for known_player in self.known_players:
                if known_player.id == receiver:
                    known_player.card_given(card)


    # Tells the player that an opponent does not own a given card
    def exclude_card(self, card, opponent_id):
        if opponent_id == self.id:
            return
        else:
            for known_player in self.known_players:
                if known_player.id == opponent_id:
                    known_player.exclude_card(card)
	
    def owns_card_of_type(self, card, receiver):
        if receiver == self.id:
            return
        else:
            for known_player in self.known_players:
                if known_player.id == receiver:
                    known_player.owns_card_of_type(card)
		
    # Find who I already know has a certain card
    def find_holder(self, card):
        if card in self.cards:
            return [self.id]
        for known_player in self.known_players:
            if card in known_player.certainCards:
                return [known_player.id]
        return [known_player for known_player in self.known_players
                if card not in known_player.certainNotCards]

    def get_owned_kinds(self):
        owned_kinds = list()
        for card in self.cards:
            if card.kind not in owned_kinds:
                owned_kinds.append(card.kind)
        return owned_kinds

    def get_requestable_cards(self):
        owned_kinds = self.get_owned_kinds()
        requestable_cards = list()
        for known_player in self.known_players:
            for card in known_player.certainCards:
                if card.kind in owned_kinds:
                    requestable_cards.append((card, known_player.id))
        return requestable_cards

    def get_number_of_requestable_cards(self, opponent):
        requestable_cards = list()
        for known_player in self.known_players:
            if known_player is opponent:
                for card in known_player.certainCards:
                    if card.kind in owned_kinds:
                        requestable_cards.append((card, known_player.id))
        return len(requestable_cards)
        
    def certain_cards(self, opponent, card):
        for known_player in self.known_players:
            if known_player.id is opponent:
                if card in known_player.certainCards:
                    return 1
                else:
                    return 0

    def certain_not_cards(self, opponent, card):
        for known_player in self.known_players:
            if known_player.id is opponent:
                if card in known_player.certainNotCards:
                    return 1
                else:
                    return 0
    
    def add_card_to_knowledge(self, opponent, card):
        for known_player in self.known_players:
            if known_player.id == opponent:
                known_player.card_given(card)
