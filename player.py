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
        self.perform_inference()
        
        #greedy strategy
        if self.strategy == 0:
            if self.certain_request():
				# Clear all full sets
                self.removeKinds(self.brain.checkAllKinds())
                
                #perform the inference
                self.perform_inference()

				# Don't allow another turn if the game is over
				# Another check for removeKinds is done in these instances due to
				# a very rare error, where about 1 in 1000 times it would not be able
				# to remove a full set. 
                if self.brain.get_valid_kinds() != []:
                    self.removeKinds(self.brain.checkAllKinds())
                    self.play()
                    
            else:
                self.removeKinds(self.brain.checkAllKinds())
                return False
        
        #silent strategy
        if self.strategy == 1:
            if self.silent_request():
			    # Clear all full sets
                self.removeKinds(self.brain.checkAllKinds())
                
                #perform the inference
                self.perform_inference()

			    # Don't allow another turn if the game is over
                if self.brain.get_valid_kinds() != []:
                    self.removeKinds(self.brain.checkAllKinds())
                    self.play()
            else:
                self.removeKinds(self.brain.checkAllKinds())
                return False        
		
		#mixed strategy
        if self.strategy == 2:
            x = random.randrange(2)
            #play greedy this turn
            if x == 0:
                if self.certain_request():
                    # Clear all full sets
                    self.removeKinds(self.brain.checkAllKinds())
                    
                    #perform the inference 
                    self.perform_inference()
                    
                    # Don't allow another turn if the game is over
                    if self.brain.get_valid_kinds() != []:
                        self.removeKinds(self.brain.checkAllKinds())
                        self.play()
                else:
                    self.removeKinds(self.brain.checkAllKinds())
                    return False
            
            #play silent this turn
            if x == 1:
                if self.silent_request():
                    # Clear all full sets
                    self.removeKinds(self.brain.checkAllKinds())
                    
                    #check for inference
                    self.perform_inference()
                    
                    # Don't allow another turn if the game is over
                    if self.brain.get_valid_kinds() != []:
                        self.removeKinds(self.brain.checkAllKinds())
                        self.play()
                else:
                    self.removeKinds(self.brain.checkAllKinds())
                    return False
        
        #play random strategy       
        if self.strategy == 3:
            if self.random_request():
			    # Clear all full sets
                self.removeKinds(self.brain.checkAllKinds())
                
                #check for inference
                self.perform_inference()
                
			    # Don't allow another turn if the game is over
                if self.brain.get_valid_kinds() != []:
                    self.removeKinds(self.brain.checkAllKinds())
                    self.play()
            else:
                self.removeKinds(self.brain.checkAllKinds())
                return False
	
	#Here we check for the inference
	#We perform the inference based on counting and whether we know a player does not own a card
    def perform_inference(self):
		#We only check for cards the player may actually ask about
        for kinds in self.brain.get_owned_kinds():
            
            #We create a list of all cards of a certain kind
            kindSet = [deck.Card(kinds, value) for value in range(4)]
            
            #we remove the cards the player already owns
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
                        self.brain.add_card_to_knowledge(possible_card_owners[0], card)
                        kindSet.remove(card)
                        #print("test1")
                        self.perform_inference()
            
            #INFERENCE BASED ON WHAT IF PLAYER HAS 3 CARDS, BUT DOES NOT KNOW LOCATION OF CARD, BUT DOES KNOW OWNS TYPE OF CARD
            kindSet = [deck.Card(kinds, value) for value in range(4)]
            for card in kindSet:
                if card in self.cards:
                    kindSet.remove(card)
                    
            if len(kindSet) is 1:
                card = kindSet[0]
                count = 0
                possible_owner = []
                for opponent in self.opponents:
                    if self.brain.owns_kind(opponent.id, card.kind):
                        possible_owner.append(opponent.id)
                if len(possible_owner) is 1:
                    self.brain.add_card_to_knowledge(possible_owner[0], card)
                    kindSet.remove(card)
                    #print("check1")
                    self.perform_inference()
            
            #INFERENCE BASED ON KNOWING THE LOCATION OF THREE CARDS
            kindSet = [deck.Card(kinds, value) for value in range(4)]
            #print(kindSet)
            for card in kindSet:
                if card in self.cards:
                    kindSet.remove(card)
            possible_owner = []
            possible_owner_already_owns_card = []
            unknown_owner = []
            

            for op in self.opponents:
                for card in kindSet:
                    if self.brain.certain_cards(op.id, card) is 1:
                        if card in kindSet:
                            kindSet.remove(card)
                            possible_owner_already_owns_card.append(op.id)
            
            for op in self.opponents:
                if self.brain.owns_kind(op, kinds):
                    possible_owner.append(op.id)
            
            if len(kindSet) == 1:
                if len(possible_owner) == 1:
                    self.brain.add_card_to_knowledge(possible_owner[0], card)
                    kindSet.remove(card)
                    #print("succes1")
                    self.perform_inference()
                else:
                    new_owner_list = []
                    for op in self.opponents:
                        if self.brain.certain_not_cards(op, card) == 0:
                            new_owner_list.append(op.id)
                    if len(new_owner_list) == 1:
                        self.brain.add_card_to_knowledge(new_owner_list[0], card)
                        kindSet.remove(card)
                        #print("success2")
                        self.perform_inference()
                    elif len(new_owner_list) > 0:
                        for op in new_owner_list:
                            unknown_cards = self.brain.known_cards_number[op] - self.brain.get_number_of_requestable_cards(op)
                            if unknown_cards == 0:
                                new_owner_list.remove(op)
                        if len(new_owner_list) == 1:
                            self.brain.add_card_to_knowledge(new_owner_list[0], card)
                            kindSet.remove(card)
                            #print("success3")
                            self.perform_inference()

        return True

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
    
    #Will only ask for cards, when location of all cards is certain. 
    #Will otherwise lie and ask for their own cards.
    def silent_request(self):
        requestable_cards = self.brain.get_requestable_cards()
        if requestable_cards == []:
            x = random.randrange(3)
            if x > 0:
                return self.random_request()
            else:
                return self.owned_request()
        
        may_request = []
        for kinds in self.brain.get_owned_kinds():
            count = 0
            for i in range(4):
                card = deck.Card(kinds, i)
                if card in self.cards:
                    count+=1
                if self.brain.check_if_in_list(card):
                    count+=1

            if count == 4:
                for i in range(4):
                    card = deck.Card(kinds, i)
                    if self.brain.check_if_in_list(card):
                        may_request.append(self.brain.return_card_in_list(card))
                        
        if may_request == []:
            x = random.randrange(3)
            if x > 0:
                return self.random_request()
            else:
                return self.owned_request()
        for opponent in self.opponents:
            if opponent.id == may_request[0][1]:
                r = opponent.draw(may_request[0][0])
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

    def owned_request(self):
        requestable_kinds = self.cards
        if requestable_kinds == []:
            return False
        hcard = random.choice(requestable_kinds)
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
