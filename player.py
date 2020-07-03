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
            
            #Here we check for all the cards currently in the list, whether we already know the location
            #and otherwise we'll check if we can determine the owner
            for card in kindSet:
                total_sum = 0
                
                #check if we already know the location. 
                for player in self.opponents:
                    total_sum += self.brain.certain_cards(player.id, card)
                    
                
                #create a list of possible owners
                possible_card_owners = []
                
                #If we don't know the location yet
                if total_sum is 0:
					
					#go through all players
                    for player in self.opponents:
						
						#when the card is not in the player's list of certain_not_cards
                        if self.brain.certain_not_cards(player.id, card) is 0:
							
							#calculate the number of unknown cards, thus cards the player has but we don't know what card it is
                            unknown_cards = self.brain.known_cards_number[player.id] - self.brain.get_number_of_requestable_cards(player.id)
                            
                            #If the number of unknown cards is larger than 0 it is possible they own this card and are appended in the list
                            if unknown_cards > 0:
                                possible_card_owners.append(player.id)
                    
                    #If there is now only one possible player left who can have the card, then that player indeed has that card            
                    if len(possible_card_owners) is 1:
                        self.brain.add_card_to_knowledge(possible_card_owners[0], card)
                        kindSet.remove(card)
                        self.perform_inference()

        return True

    # This is the greedy strategy
    def certain_request(self):
		#requests list of requestable cards, thus cards they know location of
        requestable_cards = self.brain.get_requestable_cards()
        #if list is empty, ask for a random request
        if requestable_cards == []:
            return self.random_request()
        
        #for all opponents
        for opponent in self.opponents:
			#if this opponent has a requestable cards
            if opponent.id == requestable_cards[0][1]:
				#draw that card and assert that card indeed belongs to opponent
                r = opponent.draw(requestable_cards[0][0])
                assert(r)
                #append the card to yourself and let announcer announce the card
                self.cards.append(r)
                self.announcer.card_taken(r, opponent.id, self.id)
                return True
        return False
    
    #Will only ask for cards, when location of all cards is certain. 
    #Will otherwise lie and ask for their own cards or ask for random card
    def silent_request(self):
        requestable_cards = self.brain.get_requestable_cards()
        if requestable_cards == []:
			#will ask for own or random card with 1/3 vs 2/3 chance
			#only asking own cards is really bad for performance. 
            x = random.randrange(3)
            if x > 0:
                return self.random_request()
            else:
                return self.owned_request()
        
        #list here the cards of requestable cards that player is actually allowed to ask
        may_request = []
        for kinds in self.brain.get_owned_kinds():
			#counter to keep track if location of all four cards is known
            count = 0
            for i in range(4):
                card = deck.Card(kinds, i)
                #if card is owned by themselves increase count
                if card in self.cards:
                    count+=1
                #if card location is known increase count
                if self.brain.check_if_in_list(card):
                    count+=1
			
			#when the count is 4, all locations are known
			#Here we add the cards we do not own and can request to the may request list
            if count == 4:
                for i in range(4):
                    card = deck.Card(kinds, i)
                    if self.brain.check_if_in_list(card):
                        may_request.append(self.brain.return_card_in_list(card))
        
        #If may request is empty, ask for owned or random card         
        if may_request == []:
            x = random.randrange(3)
            if x > 0:
                return self.random_request()
            else:
                return self.owned_request()
        
        #request all cards in the may request list. This works the same as the greedy request code
        for opponent in self.opponents:
            if opponent.id == may_request[0][1]:
                r = opponent.draw(may_request[0][0])
                assert(r)
                self.cards.append(r)
                self.announcer.card_taken(r, opponent.id, self.id)
                return True
        return False
        
    # Request a random card of a valid kind from a random opponent
    # Creates a random card based on the owned kinds and that chooses a random
    # value number. Then picks random opponent.
    # Then either announces giver has the card or does not have the card
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

	#Works similarly to the random request, but now picks a random card from 
	#cards that belong to the player
    def owned_request(self):
		#requestable cards are your own cards
        requestable_kinds = self.cards
        #you don't have any cards
        if requestable_kinds == []:
            return False
        #pick a random card
        hcard = random.choice(requestable_kinds)
        #pick a random opponent
        opponent = self.opponents[random.randrange(len(self.opponents))]
        r = opponent.draw(hcard)
        #opponent does not have card
        if not r:
            self.announcer.failed_request(hcard, opponent.id, self.id)
            return False
        #opponent has card (this should not be able to happen)
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
