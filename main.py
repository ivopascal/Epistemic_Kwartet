import announcer
import deck
import player
import os
	
if __name__ == "__main__":
	#Questions user how many games they want to see
    value = int(input("How many rounds do you want to play? "))
    #to keep track of total amount of wins, ties and turns
    all_winners = []
    all_ties = []
    all_turns = []
    
    #empty print to make sure the output.txt gets overwritten when running the code again
    f = open("output.txt", "w")
    print("")
    f.close()
    
    #We run through this loop for the amount of games the user wants to see
    for i in range (value):
		#print the game number, since we start counting at 0 we call our game i+1
        f = open("output.txt", "a")
        print("This is game " + str(i+1), file=f)
        f.close()
        
        #create the deck and shuffle the cards accross players
        d = deck.Deck(ncards=52)
        d.shuffle()
        cuts = d.cut(4)
        players = list()
        #create the player, the player gets a set of shuffled cards an id number and a strategy number
        for i in range(4):
            players.append(player.Player(cuts[i], nkinds=d.nkinds, id=i, strategy=i))
        
        #create the announcer and set the opponents
        a = announcer.Announcer(players)
        for i in range(4):
            players[i].intro_opponents(players[:i] + players[i+1:])
            players[i].set_announcer(a)
		
		#start at turn_number 0 and counter for the current player
        turn = 0
        player_counter = 0
        
        #print turn 0 and print the starting cards of each player.
        f = open("output.txt", "a")
        print("turn " + str(turn), file=f)
        for p in players:
            print(p.cards, file=f)
        f.close()
        
        #We start the game
        while turn >= 0:
            play = (player_counter%len(players))
            if len(players[play].cards) > 0:
				#If the player has 1 or more cards they are allowed to play
				#This code calls upon the play function, which is run in player.py
                players[player_counter % len(players)].play()
                
                #we increase the turn number and initiate the total score, which counts all removed sets
                turn += 1
                total_score = 0
                
                #we print the current turn number
                f = open("output.txt", "a")
                print("turn " + str(turn), file=f)
                f.close()
                
                
                for p in players:
					#We add the score of the players to the total_score to calculate the total number of removed sets
                    total_score += p.score
                    
                    #for each player we print their cards
                    f = open("output.txt", "a")
                    print(p.cards, file=f)
                    f.close()
                
                #If the total score is equal to the total amount of sets, the game is over.
                if total_score == d.nkinds:
                    all_turns.append(turn)
                    turn = -1
                total_score = 0
            player_counter +=1
        
        #We print that the game is finished
        f = open("output.txt", "a")
        print("The game is finished", file=f)
        print("The final score is", file=f)
        f.close()
        
        #We use these integers to determine the winning player
        count = 0    
        winner = 0
        highest_score = 0
        
        #Here we determine what the highest score was and which player number has the highest score
        for p in players:
            f = open("output.txt", "a")
            string = "Player " + str(count) + " has scored " + str(p.score) + " points"
            print(string, file=f)
            f.close()
            if p.score >= highest_score:
                highest_score = p.score
                winner = count
            
            count +=1
        
        #In case of a tie we make list with all players who have this highest score
        winners = []
        for p in players:
            if p.score == highest_score:
                winners.append(p.id)
                
		#If the length of this list of winners is equal to 1, there is only 1 winner
		#We print who won
        if len(winners) == 1:
            f = open("output.txt", "a")
            print("The winner is player " + str(winner), file=f)   
            all_winners.append(winners[0])
            f.close()
		
		#When the list is longer we print all winners
        else:
            f = open("output.txt", "a")
            print("The winners are:" , file=f)
            for win in winners:
                print("Player " + str(win), file=f)
                all_ties.append(win)
            f.close()
	
	#We calculate the total number of wins and ties each strategy has
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
    
    #calculate the average turn_length
    count = 0
    for turn in all_turns:
        count += turn
    average_turn_length = count/value
    
    #Here we print the final scoring information
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
    
        
        
