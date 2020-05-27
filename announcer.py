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

    # Tell each player that a card was taken from the giver
    #   and given to the receiver
    def card_taken(self, card, giver, receiver):
        for player in self.players:
            player.brain.card_taken(card, giver)
            player.brain.card_given(card, receiver)

    # Tell each player about a request that was failed
    # TODO: Implement knowledge that receiver has a card of given kind
    def failed_request(self, card, giver, receiver):
        for player in self.players:
            player.brain.exclude_card(card, giver)
