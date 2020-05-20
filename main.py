import announcer
import deck
import player

if __name__ == "__main__":
    d = deck.Deck(ncards=52)
    d.shuffle()
    cuts = d.cut(4)
    players = list()
    for i in range(4):
        players.append(player.Player(cuts[i], nkinds=d.nkinds, id=i))
    a = announcer.Announcer(players)
    for i in range(4):
        players[i].intro_opponents(players[:i] + players[i+1:])
        players[i].set_announcer(a)

    turn = 0
    while turn >= 0:
        players[turn % len(players)].play()
        turn += 1

        total_score = 0
        print("Turn: " + str(turn))
        for p in players:
            total_score += p.score
        if total_score == d.nkinds:
            turn = -1
        total_score = 0
