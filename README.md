### Authors: Ivo de Jong, Unmut Demirci and Marjolein Spijkerman 
### Last update: 3 July 2020, 16:11

# Logical Aspects of Multi-agent Systems: Kwartet game
Kwartet is a Dutch card game that centres around exchanging cards between players, provided that you know who that card has. This means that in order to win each player wants to maximize their knowledge of who has which cards, while minimizing the knowledge that their opponents have. This allows the player to collect more sets than their opponents and therefore win the game/

With a game as kwartet Epistemic logic is a good tool for formalizing player strategies. Each player knows their own state and might know some things about an opponent's state. Every move is a public announcement which allows the other players to learn something about the state of the game. As the possible worlds collapse the players become increasingly aware of how the cards are distributed.

# The Game

Kwartet can be played with any number of players, but the current implementation assumes 4 players. Each player gets an even split of the deck of card. The deck consists of a number of sets (in this case 13), each set having 4 members (forming a total of 52 cards). The goal for each player is to collect as many full sets as possible.

## The turns

In their turn a player has to ask one of their opponents for a specific card of a specific kind. If the opponent has that card, they give it to the player and the player gets another turn. This means that a turn can look like the following:
```python
while Card(s, m) in opponent.cards:
    opponent.cards.remove(Card(s,m))
    player.cards.add(Card(s,m))
```
Where s and v are the set and value of the card, uniquely identifying a card. The card and the opponent are re-chosen for every iteration by the player. 

### Details

There are some additional details that should be noted about these turns. Firstly, it is important to know that all moves are done in public, which has a great influence on the epistemic logic as will be discussed later.

Secondly, a player can only request cards of a set if they already have at least 1 card in that set. This means that the game naturally comes to an end when each set becomes complete under a player. For the rules in our implementation we say that when a player has completed a full set he should announce so to the other players and remove the cards from the game. 

Thirdly, players are allowed to request cards that they know they will not get. This can be asking opponent A for a card that you know opponent B has, but it could even be asking for a card that you have yourself. However, you cannot request cards which have already been removed from the game.

## The behaviour

As a consequence of these rules certain behaviour emerges. When players play randomly request cards the sets will almost certainly eventually accumulate under players and be removed from the game. As the players make better inferences of where cards may be this accumulation should occur faster. This means that the better players are at knowing where the cards they want are, there are fewer possible worlds in the Kripke model, and the game will end up being shorter.

There is an additional consideration that players may make. Players can try to minimize the knowledge of opponents, so they do not get the sets that the player wants to get. If players do this the game will comparatively consist of more turns as there is an attempt to keep more possible worlds in the Kripke model. From this we can consider that a player's (knowledge) goal should not necessarily be to minimize the number of worlds in the Kripke model, rather they should minimize the worlds they can reach while maximizing the total number of worlds.

Now that we have defined all the properties of the game in some natural language it is appropriate to show how the game runs formally in pseudocode.

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

To ease the communication in epistemic logic it is helpful to define an operator $H_i \langle t,v\rangle $ as "Player $i$ holds the card with type $t$ and value $v$". Of course, $t$ can be any of the 13 types in the game while $v$ can be any of the 4 values a type has. The new operator keeps the logic more understandable, though it can be considered as any simple atom. With this operator we can grasp with lower order logic rather than defining everything on atoms that hold these concepts in themselves. 

## Defining the game logic
In order to give a proper formalization of the logic some axioms are needed that hold necessarily. We also need to define the actions that players can make and what influence they have on knowledge that players have. Lastly, some additional knowledge that a player has is introduced.


### The axioms

For a first trivial axiom we define is that any player knows the cards that they hold. We call this the axiom of self-awareness.

$H_i \langle t,v\rangle \iff K_i H_i \langle t,v\rangle$.

We also say that it is known that each card can only exist once. We call this the axiom of singularity. $H_i \langle t,v\rangle \to \neg H_j \langle t,v\rangle$ for all $j \neq i$. By KD of course, any player that knows the antecedent also knows the consequence here. Note here that the inverse is not necessarily true, as a type may also be removed from the game, so that no-one has any card of that type. 

To support this concept we define another axiom, the axiom of (in)existence:
$ (H_{x1} \langle t, v_1\rangle \land H_{x2} \langle t, v_2 \rangle \land H_{x3} \langle t, v_3\rangle \land H_{x4} \langle t, v_4\rangle) 
\lor (\neg H_i \langle t,v_1\rangle \land \neg H_i \langle t,v_2\rangle \land \neg H_i \langle t,v_3\rangle \land \neg H_i \langle t,v_4\rangle )$ where each instance of $x$ can be any player while $i$ applies to ALL players. With this axiom the intuitive concept that either all cards of a type are held distributed across players (first part of disjunction), or no-one has any card of the type.

Lastly, in order to complete the understanding that all cards exist until they are removed, we need to add the start-state axiom. This axiom says as long as it is not common knowledge that no-one has any cards of a kind, then it must be the case that these cards are distributed over players. This means that:

$ (H_{x1} \langle t, v_1\rangle \land H_{x2} \langle t, v_2 \rangle \land H_{x3} \langle t, v_3\rangle \land H_{x4} \langle t, v_4\rangle) 
\lor C(\neg H_i \langle t,v_1\rangle \land \neg H_i \langle t,v_2\rangle \land \neg H_i \langle t,v_3\rangle \land \neg H_i \langle t,v_4\rangle)$

With this axiom we know that all cards exist at the start, and cards will only stop existing once someone has announced that they removed a set. 

### The moves

As discussed in the description of the game, players perform certain actions in their turns, but these actions release information to all players. 

First of all, we consider the information released when a player $p$ successfully takes a card from another player $q$. With this we knew that $p$ had a card from the set that they requested, and that $q$ had the requested card in question. Of course, after the request this is no-longer relevant. Instead we define that announcement to tell the current information: that $p$ has the card in question and at least one other card of that same type. Therefore, we can say that when player $p$ steals card $\langle t, v\rangle$ then:

$C (H_p \langle t, v\rangle \land H_p \langle t, u\rangle)$ where $u \neq v$.

The second part of the conjunction here is much less informative than the first part, but it is not useless. It can be used together with the axiom of singularity or the axiom of (in)existence, paired with information about other known cards to infer where a specific card is. 

The alternative move here is of course a failed request a player can make. This gives less information than the successful move, but like the second part of the conjunction above the information is not useless. When player $p$ fails to retrieve card $\langle t,v \rangle$ from opponent $q$ it becomes the case that:

$C (\neg H_q \langle t, v\rangle \land H_p \langle t, u\rangle)$

Unlike the formalization of the successful move, here $u$ can be equal to $v$. This is because players are allowed to request a card that they already have (knowing it will unsuccessful).

The last move that a player can make is to remove a set of cards from the game. Of course, they can only do this when they hold the complete set. This introduces the common knowledge that no-one has that card anymore. This can be expressed as:

$C( \neg H_x \langle t,v_1\rangle \land \neg H_x \langle t, v_2\rangle \land \neg H_x \langle t, v_2\rangle \land \neg H_x \langle t, v_3 \rangle \land \neg H_x t, v_4\rangle)$ where each instance of $x$ applies to all players.

### Counting cards

To define the logic of counting cards in the formalization that we have developed so far will lead to an explosion of the length of an expression. Therefore, to keep the notation feasible we need to define that concept of "unknown cards" in order to formalize the knowledge that an opponent has or does not have a certain number of cards that are still unknown. This concept is necessary and becomes very apparent at the end of the game, when a player has 3 cards of the last set, and one opponent has the last remaining card. For this it becomes clear that the logic must be able to incorporate the concept of an unknown card. 

We cannot define an unknown card as a special type of card, as the "unknown-ness" is not an intrinsic property of that card. Instead, we define an operator that refers from the player, to an opponent, to a number of cards. We let $U^p_{o=n}$ define that player $p$ does not know $n$ cards from opponent $o$. When an opponent has an unknown card that card can be considered as the disjunction of all possible cards, where the player does not know which card it actually is. This is intuitive to reason with, but it becomes problematic in notation, as $U^p_{o=10}$ would be an expression of 1040 atoms. We can loosely formalize this new operator with $U^p_{o=n} \iff (K_p(H_o \langle t_i,v_i \rangle \lor H_0 \langle t_j, v_j \lor ...) \land \neg K_pH_o \langle t_i, v_i\rangle \land \neg K_p\neg H_o \langle t_i, v_i\rangle \land \neg K_pH_o \langle t_j, v_j \rangle \land \neg K_p \neg H_o  \langle t_j, v_j\rangle) \land (K_p(H_o ...)) \land ...$

With the concept of an unknown card we can also reason about the lack of an unknown card. What this allows is to infer that if an opponent has 4 cards, and the player knows 4 specific cards that the opponent has, then it knows that there are no other cards.

This means that $U^p_{o=0} \to (\neg K_p H_o \langle t, v\rangle \to \neg H_o \langle t,v\rangle)$ for any $t, v$.

That is, if the opponent does not have an unknown card, then if the player doesn't know that the opponent has a card, then it must be true that he doesn't have that card.

## An example


In this example the logic of finding the last card of a given kind is demonstrated with the defined concepts above. 

We consider the situation where player 1 tries to find card $\langle 8,4\rangle$. We say that by previous actions it was learned that:

$C (H_2 \langle 8,1\rangle \land H_2 \langle 8,2\rangle \land$

$K_1 \neg H_2\langle 8, 4\rangle) \land$ 

$\neg K_1 H_3 \langle 8, 4\rangle$

Moreover, it is the case that:

$ H\_1 \langle 8,3 \rangle \land \neg H_1 \langle 8,4 \rangle \land U^1\_{3=0} \land U^1\_{4=1} $

Combining $H_1 \langle 8,3 \rangle$ with the axiom of (in)existence is but be true that:
$H_x \langle 8, 4\rangle$ for some player $x$.

This means that:
$H_1 \langle 8, 4\rangle \lor H_2 \langle 8, 4\rangle  \lor H_3 \langle 8, 4\rangle  \lor H_4 \langle 8, 4\rangle$

From $U^1_{3=0}$ and $\neg K_1 H_3 \langle 8, 4\rangle$, by the definition of $U$ it must be the case that:

$\neg H_3 \langle 8, 4\rangle$

Using A3 and $K_1 \neg H_2\langle 8, 4\rangle)$ it must be the case that $\neg H_2\langle 8, 4\rangle)$.

Lastly with $\neg H_1 \langle 8,4 \rangle$ we have found negations for 3 of the 4 components of the disjunction. From this follows that the remaining component must be true. Therefore:

$H_4 \langle 8, 4\rangle$

Since all the premises are known by player 1 (definition of $C$, A4, A5 & self-awareness) and since all the inferences are technically $\to$ relations from the premises, using KD and HS it is shown that $K_1 H_4 \langle 8, 4\rangle$

# Implementing the logic

To get this functioning in a programmed sense it is important to add additional structure to the knowledge. This helps keep algorithms for inferences sensible and keeps propositions at an acceptable complexity. The most important simplification that is made is that no logic is implemented for theory of mind. That is, players do not know, or care specifically about what other players know. While there is a smidgen of optimization that can be achieved here in strategy, it adds a tremendous amount of complexity. Instead, each player only knows their own cards and what they know.

To keep track of which cards other players have ($K_i H_o \langle t,v\rangle$) each player holds a list of the cards of each opponent that they know. The other relevant type of information is the knowledge of which cards opponents do not have ($K_i \neg H_o \langle t,v \rangle$), this is held in a similar but distinct list. What remains are the cards that a player may or may not have. This does need to be tracked as it is simply all valid cards that have no known location, which can be inferred on the fly. For this inference the player does need to keep a list of which cards are removed, so they can use the axiom of (in)existence and the axiom of start-state together with this list to determine which cards are valid. 

A player should also be aware of how many cards the other players have, so they are able to determine the $U$ operator and make inferences based on the number of remaining cards. In order to avoid storing any complicated disjunctions that last list that players can keep is the list of known kinds, which is the disjunction of a player holding at least one card of a given type as discussed before. 

Using these encodings of the current knowledge further inferences can be made about which card is where.

## Implementing the inferences

To implement the logical inference the program goes through the following steps for each player:
Firstly, we go through all the card types the player owns. As these are the cards the player may ask about. 
For each card type the player owns, we create a list of cards of that type the player does not have yet. Then we remove all the cards where the player does already know who has that card. Thus, we are left with a list of cards where the owner of said card is unknown.
Then for each card, we check for each opponent if that card is in their list of cards they do not have and whether they have any unknown cards. Thus, we check if the number of cards they have is larger than the number of cards the player knows they have. Meaning it is possible that they have that card. 
All the players who we know do not “not have” the card, and still have unknown cards are added to a list with possible owners. 
If the length of this possible owner list is equal to 1, we can determine that that player, has indeed the card. 

The player will perform this inference, both at the start of their turn and after making a successful move. 


# Strategies

With the knowledge the players can now obtain they are able to maximize their understanding of which card is where. However, this does not yet determine which requests they should be making. Below we show some strategies, so that we may compare their performance when they are pitted against one another.

## Random requests

The first strategy is somewhat of a "dummy" strategy. It will simply ask any random opponent for any random card from a type that they are allowed to request. Of course, this is a very ineffective strategy as there is only a 1/4 chance of making a successful request, and an even smaller chance to complete a set on any given turn.

## Greedy requests

The greedy strategy takes more advantage of the knowledge and logic that is defined for them. Rather than ask for any random card they only ask for the cards that they know a certain player has. This has the advantage of actually being able to complete sets when they know the location of each card in that set. The disadvantage to this however is that players may give additional information to other players about which card is where, and since the other players are perfect logicians with perfect memory, they can take back all these cards.

## Silent requests

The silent strategy is similar to the greedy strategy. The main difference is that they will only ask for a card that they know a certain player has when they know the position for all four cards. In the cases where they only know the position of three or less cards of a set they own partly, they will ask 2/3 of the times for a random card or 1/3 of the times for a card they own themselves. They will thus lie and ask for their own cards more often than in the regular random request, to avoid other players from finding out what their cards are.

## Mixed request

As a fourth possible request type, we use a mix of the greedy and the silent request. Half of the times the player will play as if they are using the greedy strategy and the other half of the times they play as if using the silent strategy. This mixed strategy is added as a valid strategy for the fourth player to use, furthermore it can be used to see if a mixed strategy would be more useful. 

# Results
We ran the program for a total of 10.000 rounds. 
For each round we kept track of the winners, the amount of turns and the average number of successful inferences per game. <br>
We created an overview of the number of times each strategy had a win and each time a strategy had a tied win. <br>
We also calculated the average number of successful inferences performed per game and the average turn length per game. <br>
This led to the following data: <br> <br>
8313 games resulted in having one winner and the other 1687 games resulted in having two or more winners.<br>
The Greedy strategy had 5597 out of 10000 wins<br>
The Silent strategy had 781 out of 10000 wins<br>
The Mixed strategy had 1933 out of 10000 wins<br>
The Random strategy had 2 out of 10000 wins<br>
The Greedy strategy had 1545 ties<br>
The Silent strategy had 683 ties<br>
The Mixed strategy had 1290 ties<br>
The Random strategy had 1 ties<br>
<br>
The average turn length is 137.2307<br>
The average number of inferences per game is 24.4148. <br>
<br>
The circle diagrams below, show the percentages that each strategy won for both normal wins and the runs that resulted in a tie. <br>
![Alt text](numberofwins.png?raw=true "Title")
![Alt text](numberofties.png?raw=true "Title")


# Analysis of results
First of all, we looked at the performance of the code. The code runs quite fast. For a total of 50 rounds, the code would take 1m31.611s real time, 0m35.480s user time and 
0m0.828s system time to run for the full set of 50 games, ending with an overview of the wins and tied wins. This includes printing all the cards each player has for each turn in a .txt file. <br>

Furthermore, to test whether using the inference indeed added correct card-player combinations we used an assert function. In the greedy strategy and the silent strategy, we create a list with requestable cards, cards where we know the location of, after taking this card we use an assert() function to check whether this card indeed exists on the location of the original player. If it does not, the program will output an error and stops running. When running the code for 10.000 rounds, we never came across an error produced by the assert() function. Thus, we can assume the implementation of the inference works correctly. <br><br>
Secondly, when looking at the performance of the different strategies, the greedy strategy is the clear winner. The Mixed strategy comes at the second place, followed by the Silent strategy and finally the Random Strategy. <br>

The greedy strategy is the most aggressive strategy and takes any card where they know the location, thus it will constantly take any card it can find as soon as it sees the opportunity. The silent strategy on the other hand, waits until they can find the location of all four cards, meaning that the greedy strategy can more quickly get the cards before the silent strategy had the time to get the cards. The mixed strategy uses either the greedy or the silent strategy 50% of the times. Since the greedy strategy performs way better than the silent strategy, the mixed strategy ends up in the middle performance-wise. Lastly, the random strategy does not use any knowledge or logic at all and since kwartet is mostly not a luck-based game, they will loose almost all of the times. <br>
## Further Research
It would be interesting to look at the same program using some different settings. For example, we can run the game with only three players. This could influence how many inferences can be made in the game and will most likely also decrease the number of turns needed to finish the game. This is because with only three players, there are less options left for whom can own what card, so guessing will also have better odds. Another thing that could be changed for comparison is the strategies each player uses, instead of using four different strategies, it can be interesting to let all players for example use the same strategy, and see how this influence the average number of turns. It can also be interesting to change the order of the players, the four strategies are now always ordered in the same order. So, the greedy strategy is always player 1 and they get the first turn. It can be interesting to see if the percentage of wins for each strategy may differ when the turn order is changed. <br> <br>
Some things that would be good to change in the greedy function is the following. At the moment, when the greedy function does not have any cards they can ask for with certainty, they ask for a random card. This means they can ask for a card they already own, or they could ask for a card they already know a player does not have. This is not efficient gameplay behaviour for the greedy strategy. It would be better to pick a card they don't have yet, create a list with who can possibly own the card, thus someone who does have unknown cards and someone of whom we know they do not "not have" the card, and than randomly pick on of the owners. In this case there are always multiple owners to choose from, as when there was only one possible pick, it would have been found by the inference function before the player would decide on a card. Implementing this, would make the greedy strategy an even better player and this would make the greedy player act more like a regular person player kwartet. <br>





