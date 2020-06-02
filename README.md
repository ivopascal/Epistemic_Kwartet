

Kwartet is a Dutch card game that centers around exchanging cards between players, provided that you know who that card has. This means that in order to win each player wants to maximize their knowledge of who has which cards, while minimizing the knowledge that their opponents have. This allows the player to collect more sets than their opponents and therefore win the game/

With a game as kwartet Epistemic logic is a good tool for formalizing player strategies. Each player knows their own state, and might now some things about an opponents state. Every move is a public announcement which allows the other players to learn something about the state of the game. As the possible worlds collapse the players become increasingly aware of how the cards are distributed.

# The Game

Kwartet can be played with any number of players, but the current implementation assumes 4 players. Each player gets an even split of the deck of card. The deck consists of a number of sets (in this case 13), each set having 4 members (forming a total of 52 cards). The goal for each player is to collect as many full sets as possible.

## The turns

In their turn a player has to ask one of their opponents for a specific card of a specific kind. If the opponent has that card they give it to the player and the player gets another turn. This means that a turn can look like the following:
```
while Card(s, m) in opponent.cards:
    opponent.cards.remove(Card(s,m))
    player.cards.add(Card(s,m))
```
Where s and v are the set and value of the card, uniquely identifying a card. The card and the opponent are re-chosen for every iteration by the player. 

### Details

There's some additional details that should be noted about these turns. Firstly it is important to know that all moves are done in public, which has a great influence on the epistemic logic as will be discussed later.

Secondly, a player can only request cards of a set if they already have at least 1 card in that set. This means that the game naturally comes to an end when each set becomes complete under a player. For the rules in our implementation we say that when a player has completed a full set he should announce so to the other players and remove the cards from the game. 

Third, players are allowed to requests cards that they know they will not get. This can be asking opponent A for a card that you know opponent B has, but it could even be asking for a card that you have yourself. However, you cannot request cards which have already been removed from the game.

## The behaviour

As a consequence of these rules certain behaviour emerges. When players play randomly request cards the sets will almost certainly eventually accumulate under players and be removed from the game. As the players make better inferences of where cards may be this accumulation should occur faster. This means that the better players are at knowing where the cards they want are, there are fewer possible worlds in the Kripke model, and the game will end up being shorter.

There is an additional consideration that players may make. Players can try to minimize the knowledge of opponents so they don't get the sets that the player wants to get. If players do this the game will comparatively consist of more turns as there is an attempt to keep more possible worlds in the Kripke model. From this we can consider that a player's (knowledge) goal should not necessarily be to minimize the number of worlds in the Kripke model, rather they should minimize the worlds they can reach while maximizing the total number of worlds.

Now that we have defined all the properties of the game in some natural language it is appropriate to show how the game runs formally in psuedocode.

```python
while CardsInGame:
    foreach player in Players:
        while not endTurn:
            s, v, opponent = player.pickRequest()
            if opponent.hasCard(Card(s,v)):
                opponent.removeCard(Card(s,v))
                player.addCard(Card(s,v))
                ANNOUNCE(player took Card(s,v) from opponent)
            else:
                ANNOUNCE(player failed to take Card(s,v) from opponent)
                endTurn = true
                
            fullSet = player.getFullSet()
            if fullSet != None:
                ANNOUNCE(player removed set fullSet)
                player.removeCards(fullSet):
                player.points += 1
```

The above example includes all the announcements that would be made during the game, which also gives the players some opportunity to learn about the state of the game. Nonetheless, all the most interesting parts are omitted from the example above as they really exist in how `player.pickRequest()` actually determines who to ask for which card.

# The logic

To ease the communication in epistemic logic it is helpful to define an operator $H_i p$.
