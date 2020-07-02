
def find_correct_player_information(turn, player):

    correct_line = -100
    needed_line = "turn " + str(turn)
    print(needed_line)
    with open ("output.txt") as fp:
        for i, line in enumerate(fp):
            line = line[:-1]
            if line == needed_line:
                correct_line = i
                    
            if i == (correct_line + player):
                return line


string = find_correct_player_information(124, 1)
print(string)
