import announcer
import deck
import player

import colorama
from colorama import Fore, Style
import os
	
if __name__ == "__main__":
    value = int(input("How many rounds do you want to play? "))
    #value = 5
    all_winners = []
    all_ties = []
    all_turns = []
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
        print("turn " + str(turn))
        for player in players:
            print(player.cards)
			
        while turn >= 0:
            play = (player_counter%len(players))
            if len(players[play].cards) > 0:
                players[player_counter % len(players)].play()
                turn += 1

                total_score = 0
                print("turn " + str(turn))
                #print("")
                #print(Fore.MAGENTA + "Turn: " + str(turn))
                #print(Style.RESET_ALL)
                num = 0
                for p in players:
                    total_score += p.score
                    print(p.cards)
                    #print(p.brain.known_cards_number[num])
                    #print("player " + str(num) + " has") 
                    #print(Fore.CYAN)
                    #print(p.cards)
                    #print(Style.RESET_ALL)
                    #print(p.brain.get_owned_kinds())
                    num+=1
                if total_score == d.nkinds:
                    all_turns.append(turn)
                    turn = -1
                total_score = 0
            player_counter +=1
        
        print("The game is finished")
        print("The final score is")
        #print(Fore.BLUE + "The final score is")
        count = 0    
        winner = 0
        highest_score = 0
        for p in players:
            string = "Player " + str(count) + " has scored " + str(p.score) + " points"
            print(string)
            #print(Fore.CYAN + string)
            #print(Style.RESET_ALL)
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
    
    count = 0
    for turn in all_turns:
        count += turn
    average_turn_length = count/value
    
    print("We played " + str(value) + " rounds")
    print("The Greedy strategy had " + str(greedy) + " out of " + str(value) + " wins")
    print("The Silent strategy had " + str(silent) + " out of " + str(value) + " wins")
    print("The Mixed strategy had " + str(mixed) + " out of " + str(value) + " wins")
    print("The Random strategy had " + str(random) + " out of " + str(value) + " wins")
    print("The Greedy strategy had " + str(tgreedy) + " ties")
    print("The Silent strategy had " + str(tsilent) + " ties")
    print("The Mixed strategy had " + str(tmixed) + " ties")
    print("The Random strategy had " + str(trandom) + " ties")
    print("The average turn length is " + str(average_turn_length))
    
    
        
        
