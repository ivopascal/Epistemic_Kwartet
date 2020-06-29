import announcer
import deck
import player

import colorama
from colorama import Fore, Style

	
if __name__ == "__main__":
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
        if p.score > highest_score:
            highest_score = p.score
            winner = count
        
        count +=1
    print("The winner is player " + str(winner))
        
        
