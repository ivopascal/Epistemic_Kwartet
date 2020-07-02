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
            player.brain.known_cards_number[id] -= 4
        string = "Quartet number " + str(kind) + " has been removed from player " + str(id) + ", player " + str(id) + " now has " + str(player.brain.known_cards_number[id]) + " cards."
        #print(string)

    # Tell each player that a card was taken from the giver
    #   and given to the receiver
    def card_taken(self, card, giver, receiver):
        for player in self.players:
            player.brain.card_taken(card, giver)
            player.brain.card_given(card, receiver)
            player.brain.owns_card_of_type(card, receiver)
            player.brain.known_cards_number[giver] -= 1
            player.brain.known_cards_number[receiver] +=1
        #print(card.kind)
        string = "Of quartet number " + str(card.kind) + " card number " + str(card.value) + " has been removed from player " + str(giver) + " and has been given to player " + str(receiver) + ". Player " + str(receiver) + " now has " + str(player.brain.known_cards_number[receiver]) + " cards and player " + str(giver) + " now has " + str(player.brain.known_cards_number[giver]) + " cards." 
        #print(string)

    # Tell each player about a request that was failed
    # TODO: Implement knowledge that receiver has a card of given kind
    def failed_request(self, card, giver, receiver):
        for player in self.players:
            player.brain.exclude_card(card, giver)
            player.brain.owns_card_of_type(card, receiver)
