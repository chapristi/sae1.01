class Player:
    id : int
    name : str
    scoreRiddle: int
    scoreTtt : int
    scoreMatches : int
    scoreP4 : int

class CurrentPlayers:
    player1 : Player
    player2 : Player


class Players:
    tabPlayers: list[Player]