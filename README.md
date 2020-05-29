
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

Secondly, a player can only request cards of a set if they already have at least 1 card in that set. This means that the game naturally comes to an end when each set becomes complete under a single player. For the rules in our implementation we say that when a player has completed a full set he should announce so to the other players and remove the cards from the game. 
