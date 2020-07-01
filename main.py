import announcer
import deck
import player

import colorama
from colorama import Fore, Style
import os

if __name__ == "__main__":
    value = int(input("How many rounds do you want to play? "))
    all_winners = []
    all_ties = []
    for i in range (value):
        d = deck.Deck(ncards=52)
        d.shuffle()
        cuts = d.cut(4)
        players = list()
        for i in range(4):
            players.append(player.Player(cuts[i], nkinds=d.nkinds, id=i, strategy=i))
        a = announcer.Announcer(players)
        for i in range(4):
            players[i].intro_opponents(players[:i] + players[i+1:])
            players[i].set_announcer(a)

        turn = 0
        player_counter = 0
        while turn >= 0:
            play = (player_counter%len(players))
            #print(len(players[play].cards))
            if len(players[play].cards) > 0:
                players[player_counter % len(players)].play()
                turn += 1

                total_score = 0
                print("")
                print(Fore.MAGENTA + "Turn: " + str(turn))
                print(Style.RESET_ALL)
                num = 0
                for p in players:
                    total_score += p.score
                    #print(p.brain.known_cards_number[num])
                    print("player " + str(num) + " has")
                    print(Fore.CYAN)
                    print(p.cards)
                    print(Style.RESET_ALL)
                    print(p.brain.get_owned_kinds())
                    num+=1
                if total_score == d.nkinds:
                    turn = -1
                total_score = 0
            player_counter +=1

        print(Fore.BLUE + "The final score is")
        count = 0
        winner = 0
        highest_score = 0
        for p in players:
            string = "Player " + str(count) + " has scored " + str(p.score) + " points"
            print(Fore.CYAN + string)
            print(Style.RESET_ALL)
            if p.score >= highest_score:
                highest_score = p.score
                winner = count

            count +=1

        winners = []
        for p in players:
            if p.score == highest_score:
                winners.append(p.id)


        if len(winners) == 1:
            print("The winner is player " + str(winner))
            all_winners.append(winners[0])

        else:
            print("The winners are:" )
            for win in winners:
                print("Player " + str(win))
                all_ties.append(win)

    greedy = 0
    silent = 0
    mixed = 0
    random = 0
    tgreedy = 0
    tsilent = 0
    tmixed = 0
    trandom = 0
    for winner in all_winners:
        if winner == 0:
            greedy +=1
        elif winner == 1:
            silent +=1
        elif winner == 2:
            mixed +=1
        elif winner == 3:
            random +=1

    for winner in all_ties:
        if winner == 0:
            tgreedy +=1
        elif winner == 1:
            tsilent +=1
        elif winner == 2:
            tmixed +=1
        elif winner == 3:
            trandom +=1

    print("We played " + str(value) + " rounds")
    print("The Greedy strategy had " + str(greedy) + " out of " + str(value) + " wins")
    print("The Silent strategy had " + str(silent) + " out of " + str(value) + " wins")
    print("The Mixed strategy had " + str(mixed) + " out of " + str(value) + " wins")
    print("The Random strategy had " + str(random) + " out of " + str(value) + " wins")
    print("The Greedy strategy had " + str(tgreedy) + " ties")
    print("The Silent strategy had " + str(tsilent) + " ties")
    print("The Mixed strategy had " + str(tmixed) + " ties")
    print("The Random strategy had " + str(trandom) + " ties")

    text = f''' 
   We played  {str(value)}  rounds
   The Greedy strategy had {str(greedy)}  out of  {str(value)}  wins
   The Silent strategy had {str(silent)}  out of  {str(value)}  wins
   The Mixed strategy had  {str(mixed)} out of  {str(value)}  wins
   The Random strategy had  {str(random)} out of  {str(value)}  wins
   The Greedy strategy had {str(tgreedy)} ties
   The Silent strategy had  {str(tsilent)}  ties
   The Mixed strategy had   {str(tmixed)}   ties
   The Random strategy had {str(trandom)}  ties
'''


    with open('secondfile.txt', 'w') as file:
        file.write(text)


    text = f''' 
   The winner is player  {str(winner)}
   
'''


    with open('secondfile.txt', 'w') as file:
        file.write(text)