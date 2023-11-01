class Player:
    id : int
    name : str
    playerNumber : int
    scoreRiddle: int
    scoreTtt : int
    scoreMatches : int
    scoreP4 : int

def playerInit(player : Player, id : int, name : str, scoreRiddle : int, scoreTtt:int, scoreMatches : int, scoreP4 : int):
    player.id = id
    player.name = name
    player.scoreRiddle = scoreRiddle
    player.scoreTtt = scoreTtt
    player.scoreMatches = scoreMatches
    player.scoreP4 = scoreP4

class CurrentPlayers:
    player1 : Player
    player2 : Player

def currentPlayersInit(curentPlayers : CurrentPlayers, player1 : Player, player2 : Player):
    curentPlayers.player1 = player1
    curentPlayers.player2 = player2
    curentPlayers.player1.playerNumber = 2
    curentPlayers.player2.playerNumber = 3
