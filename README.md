

Kwartet is a Dutch card game that centers around exchanging cards between players, provided that you know who that card has. This means that in order to win each player wants to maximize their knowledge of who has which cards, while minimizing the knowledge that their opponents have. This allows the player to collect more sets than their opponents and therefore win the game/

With a game as kwartet Epistemic logic is a good tool for formalizing player strategies. Each player knows their own state, and might now some things about an opponents state. Every move is a public announcement which allows the other players to learn something about the state of the game. As the possible worlds collapse the players become increasingly aware of how the cards are distributed.

# The Game

Kwartet can be played with any number of players, but the current implementation assumes 4 players. Each player gets an even split of the deck of card. The deck consists of a number of sets (in this case 13), each set having 4 members (forming a total of 52 cards). The goal for each player is to collect as many full sets as possible.

## The turns

In their turn a player has to ask one of their opponents for a specific card of a specific kind. If the opponent has that card they give it to the player and the player gets another turn. This means that a turn can look like the following:
```python
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

To ease the communication in epistemic logic it is helpful to define an operator $H_i \langle t,v\rangle $ as "Player $i$ holds the card with type $t$ and value $v$". Of course $t$ can be any of the 13 types in the game while $v$ can be any of the 4 values a type has. The new operator keeps the logic more understandable, though it can be considered as any simple atom. With this operator we can grasp with lower order logic rather than defining everything on atoms that hold these concepts in themselves. 

## Defining the game logic
In order to give a proper formalization of the logic some axioms are needed that hold necessarily. We also need to define the actions that players can make and what influence they have on knowledge that players have. Lastly, some additional knowledge that a player has is introduced.


### The axioms

For a first trivial axiom we define is that any player knows the cards that they hold. We call this the axiom of self-awareness.

$H_i \langle t,v\rangle \iff K_i H_i \langle t,v\rangle$.

We also say that it is known that each card can only exist once. We call this the axiom of singularity. $H_i \langle t,v\rangle \to \neg H_j \langle t,v\rangle$ for all $j \neq i$. By KD ofcourse any player that knows the antecedent also knows the consequence here. Note here that the inverse is not necessarily true, as a type may also be removed from the game, so that no-one has any card of that type. 

To support this concept we define another axiom, the axiom of (in)existence:
$ (H_x \langle t, v_1\rangle \land H_x \langle t, v_2 \rangle \land H_x \langle t, v_3\rangle \land H_x \langle t, v_4\rangle) 
\lor (\neg H_i \langle t,v_1\rangle \land \neg H_i \langle t,v_2\rangle \land \neg H_i \langle t,v_3\rangle \land \neg H_i \langle t,v_4\rangle )$ where each instance of $x$ can be any player while $i$ applies to ALL players. With this axiom the intuitive concept that either all cards of a type are held distributed across players (first part of disjunction), or no-one has any card of the type.

Lastly, in order to complete the understanding that all cards exist until they are removed we need to add the start-state axiom. This axiom says as long as it is not common knowledge that no-one has any cards of a kind, then it must be the case that these cards are distributed over players. This means that:

$ (H_x \langle t, v_1\rangle \land H_x \langle t, v_2 \rangle \land H_x \langle t, v_3\rangle \land H_x \langle t, v_4\rangle) 
\lor C(\neg H_i \langle t,v_1\rangle \land \neg H_i \langle t,v_2\rangle \land \neg H_i \langle t,v_3\rangle \land \neg H_i \langle t,v_4\rangle)$

With this axiom we know that all cards exist at the start, and cards will only stop existing once someone has announced that they removed a set. 

### The moves

As discussed in the description of the game, players perform certain actions in their turns, but these actions release information to all players. 

First we consider the information released when a player $p$ succesfully takes a card from another player $q$. With this we knew that $p$ had a card from the set that they requested, and that $q$ had the requested card in question. Ofcourse after the request this is no-longer relevant. Instead we define that announcement to tell the current information: that $p$ has the card in question and at least one other card of that same type. Therefore, we can say that when player $p$ steals card $\langle t, v\rangle$ then:

$C (H_p \langle t, v\rangle \land H_p \langle t, u\rangle)$ where $u \neq v$.

The second part of the conjunction here is much less informative than the first part, but it is not useless. It can be used together with the axiom of singularity or the axiom of (in)existence, paired with information about other known cards to infer where a specific card is. 

The alternative move here is ofcourse a failed request a player can make. This gives less information than the succesful move, but like the second part of the conjunction above the information is not useless. When player $p$ fails to retrieve card $\langle t,v \rangle$ from opponent $q$ it becomes the case that:

$C (\neg H_q \langle t, v\rangle \land H_p \langle t, u\rangle)$

Unlike the formalization of the succesfull move, here $u$ can be equal to $v$. This is because players are allowed to request a card that they already have (knowing it will unsuccesful).

The last move that a player can make is to remove a set of cards from the game. Ofcourse they can only do this when they hold the complete set. This introduces the common knowledge that no-one has that card anymore. This can be expressed as:

$C( \neg H_x \langle t,v_1\rangle \land \neg H_x \langle t, v_2\rangle \land \neg H_x \langle t, v_2\rangle \land \neg H_x \langle t, v_3 \rangle \land \neg H_x t, v_4\rangle)$ where each instance of $x$ applies to all players.

### Counting cards

To define the logic of counting cards in the formalization that we have developped so far will lead to an explosion of the length of an expression. Therefore, to keep the notation feasible we need to define that concept of "unkown cards" in order to formalize the knowledge that an opponent has or doesn't have a certain number of cards that are sitll unknown. This concept is necessary and becomes very apparent at the end of the game, when a player has 3 cards of the last set, and one opponent has the last remaining card. For this it becomes clear that the logic must be able to incorporate the concept of an unknown card. 

We may define card $\langle x,x\rangle$ as the "unkown card", and we can define a number of unkown cards as $\langle x,x\rangle_n$. When an opponent has an unknown card that card can be considered as the disjunction of all possible cards, where the player does not know which card it actually is. This is intuitive to reason with, but it becomes problematic in notation, as $H_2 \langle x,x\rangle_10$ would be an expression of 1040 atoms. 

With the concept of an unknown card we can also reason about the lack of an unknown card. What this allows is to infer that if an opponent has 4 cards, and the player knows 4 specific cards that the opponent has, then it knows that there are no other cards.

This means that $K_p H_o \langle x,x\rangle_0 \to (\neg K_p H_o \langle t, v\rangle \to \neg H_o \langle t,v\rangle)$ for any $t, v$.

That is, if the opponent doesn't have an unknown card, then if the player doesn't know that the opponent has a card, then it must be true that he doesn't have that card.

## Some examples

Below we define some examples of inferences that can be made by the players using the axioms and knowledge that they may have from moves players made previously.

### Last of the kind

In this example the logic of finding the last card of a given kind is demonstrated with the defined concepts above. 




