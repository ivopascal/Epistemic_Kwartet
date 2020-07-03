import main
class Announcer:
    '''
    The announcer class is intended to manage
        all the Public Announcements that are made.
    A player can tell the announcer that a certain action was made,
    and then the announcer can tell each player about the action that was made.

    This seperation keeps the operations of
        announcing and listening out of the Player class.
    '''
    def __init__(self, players):
        self.players = players

    # Tells all players that a Kind has been removed from the game
    def announce_remove_kind(self, kind, id):
        for player in self.players:
            player.brain.remove_kind(kind, id)
            
            #Keep track of number of cards
            player.brain.known_cards_number[id] -= 4

    # Tell each player that a card was taken from the giver
    #   and given to the receiver
    def card_taken(self, card, giver, receiver):
        for player in self.players:
            player.brain.card_taken(card, giver)
            player.brain.card_given(card, receiver)
            player.brain.owns_card_of_type(card, receiver)
            
            #Keep track of number of cards
            player.brain.known_cards_number[giver] -= 1
            player.brain.known_cards_number[receiver] +=1


    # Tell each player about a request that was failed
    # The giver thus does not have the card and the receiver owns a card of that type
    def failed_request(self, card, giver, receiver):
        for player in self.players:
            player.brain.exclude_card(card, giver)
            player.brain.owns_card_of_type(card, receiver)
