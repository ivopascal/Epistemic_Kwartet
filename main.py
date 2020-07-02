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
    all_turns = []
    f = open("output.txt", "w")
    print("")
    f.close()
    for i in range (value):
        f = open("output.txt", "a")
        print("This is game " + str(i+1), file=f)
        f.close()
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
        f = open("output.txt", "a")
        print("turn " + str(turn), file=f)
        for p in players:
            print(p.cards, file=f)
        f.close()
        
        while turn >= 0:
            play = (player_counter%len(players))
            if len(players[play].cards) > 0:
                players[player_counter % len(players)].play()
                turn += 1

                total_score = 0
                f = open("output.txt", "a")
                print("turn " + str(turn), file=f)
                f.close()
                num = 0
                for p in players:
                    total_score += p.score
                    f = open("output.txt", "a")
                    print(p.cards, file=f)
                    f.close()
                    num+=1
                if total_score == d.nkinds:
                    all_turns.append(turn)
                    turn = -1
                total_score = 0
            player_counter +=1
        
        f = open("output.txt", "a")
        print("The game is finished", file=f)
        print("The final score is", file=f)
        f.close()
        count = 0    
        winner = 0
        highest_score = 0
        for p in players:
            f = open("output.txt", "a")
            string = "Player " + str(count) + " has scored " + str(p.score) + " points"
            print(string, file=f)
            f.close()
            if p.score >= highest_score:
                highest_score = p.score
                winner = count
            
            count +=1
        
        winners = []
        for p in players:
            if p.score == highest_score:
                winners.append(p.id)
                

        if len(winners) == 1:
            f = open("output.txt", "a")
            print("The winner is player " + str(winner), file=f)   
            all_winners.append(winners[0])
            f.close()
                 
        else:
            f = open("output.txt", "a")
            print("The winners are:" , file=f)
            for win in winners:
                print("Player " + str(win), file=f)
                all_ties.append(win)
            f.close()
		
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
    
    count = 0
    for turn in all_turns:
        count += turn
    average_turn_length = count/value
    
    f = open("output.txt", "a")
    print("We played " + str(value) + " rounds", file=f)
    print("The Greedy strategy had " + str(greedy) + " out of " + str(value) + " wins", file=f)
    print("The Silent strategy had " + str(silent) + " out of " + str(value) + " wins", file=f)
    print("The Mixed strategy had " + str(mixed) + " out of " + str(value) + " wins", file=f)
    print("The Random strategy had " + str(random) + " out of " + str(value) + " wins", file=f)
    print("The Greedy strategy had " + str(tgreedy) + " ties", file=f)
    print("The Silent strategy had " + str(tsilent) + " ties", file=f)
    print("The Mixed strategy had " + str(tmixed) + " ties", file=f)
    print("The Random strategy had " + str(trandom) + " ties", file=f)
    print("The average turn length is " + str(average_turn_length), file=f)
    f.close()
    
        
        
