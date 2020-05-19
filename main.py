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
        players.append(player.Player(cuts[i]))
