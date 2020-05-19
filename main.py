import deck
import player


def main():
    print("Hello World!")


if __name__ == "__main__":
    d = deck.Deck(ncards=52)
    d.shuffle()
    cuts = d.cut(4)
    players = list()
    for i in range(4):
        players.append(player.Player(cuts[i], ntypes=d.ntypes(), id=i))
    for i in range(4):
        players[i].intro_opponents(players[:i] + players[i+1:])

    turn = 0
    while turn >= 0:
        players[turn].play()
        turn += 1
        if turn == 4:
            turn = 0

        total_score = 0
        for p in players:
            total_score += p.score
        if total_score == d.ntypes():
            turn = -1
        total_score = 0
