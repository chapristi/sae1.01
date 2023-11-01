#from player import CurrentPlayers
from game_match import GameMatch, gameMatchInit
from colors import set_color_green,set_color_red,set_color_yellow
from input_checker import isDigit
from sqlite3 import Connection
from player import *
from sql_commands import addPoint
from helperPlayer import getOtherPlayer

def displayStartingMenu() -> None:
    print(set_color_green("Bienvenue sur le jeu des Allumettes etes vous pret a jouer?"))
    print(set_color_green("Chargement..."))

def displayWin(winner : Player, currentPLayers: CurrentPlayers,gameMatch : GameMatch) -> None:
    looser : Player

    looser = getOtherPlayer(currentPLayers,winner)
    print(set_color_green("Bravo c'est ("+  winner.name + ") qui l'emporte et gagne "+ str(gameMatch.pointWin)+" points"))
    print(set_color_yellow("Dommage c'est (" + looser.name + ") qui a perdu mais remporte "+ str(gameMatch.pointWin)+" points"))

def pointsRepartition(gameMatch : GameMatch,conn :Connection,currentPlayers:CurrentPlayers,winner:Player):
    looser : Player

    looser = getOtherPlayer(currentPlayers,winner)
    addPoint(winner.id,gameMatch.pointWin,conn,gameMatch.colName)
    addPoint(looser.id,gameMatch.pointLoose,conn,gameMatch.colName)
  
def drawMatches(nb : int) -> None:
    matches : list[str]
    i: int

    i = 0
    matches = [
         set_color_red("█"),
         set_color_yellow ("█"),
         set_color_yellow ("█"),
         set_color_yellow ("█"),
         set_color_yellow ("█"),
    ]
    for i in range(0,5):
        print()
        for _ in range(0,nb):
            print(matches[i] + " ",end="")
    print()


    
def game(currentPlayers : CurrentPlayers, conn : Connection) -> None:
    """
        currentPLayers : CurrentPlayers
    """
    gameMatch : GameMatch
    currPlayer : Player
    choice  : str

    currPlayer = currentPlayers.player1
    gameMatch = GameMatch()
    gameMatchInit(gameMatch)
    displayStartingMenu()

    while gameMatch.numberOfMatches > 0:
        drawMatches(gameMatch.numberOfMatches)
        print(set_color_green(currPlayer.name), "à vous de jouer")
        choice = input("choisissez entre " + set_color_yellow("1,2 ou 3") +" allumettes à retirer ")
        
        while not isDigit(choice) or int(choice) < 1 or int(choice) > 3:
            choice = input(
                set_color_yellow("⚠️ choisissez entre 1,2 ou 3 allumettes à retirer")
            )
        gameMatch.numberOfMatches -= int(choice)
        currPlayer = getOtherPlayer(currentPlayers,currPlayer)

    displayWin(currPlayer,currentPlayers,gameMatch)
    pointsRepartition(gameMatch,conn,currentPlayers,currPlayer)
              



