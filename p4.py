from gameP4 import GameP4,gameP4Init
from player import CurrentPlayers,Player
from colors import *
from input_checker import isDigit
from sql_commands import addPoint
from sqlite3 import Connection
from helperPlayer import getOtherPlayer

def displayStartingMenu():
    print(set_color_green("Bienvenue à vous dans le jeu du puissance 4"))
    print(set_color_green("Chargement..."))

def checkWin(gameP4 : GameP4, currentPlayer : Player)->bool:
    i : int
    j : int
    isWin : bool
    currentPlayerNumber : int

    i = 0
    j = 0
    isWin = False
    currentPlayerNumber = currentPlayer.playerNumber

    while i < gameP4.size_y - 3 and not isWin:
        j = 0
        while j < gameP4.size_x:
            if (gameP4.plate[i][j] == currentPlayerNumber and gameP4.plate[i+1][j] == currentPlayerNumber
                and gameP4.plate[i+2][j] == currentPlayerNumber and gameP4.plate[i+3][j] == currentPlayerNumber):
                isWin = True
            j += 1
        i += 1

    i = 0
    while i < gameP4.size_y and not isWin:
        j = 0
        while j < gameP4.size_x - 3 and not isWin:
            if (gameP4.plate[i][j] == currentPlayerNumber and gameP4.plate[i][j+1] == currentPlayerNumber
                and gameP4.plate[i][j+2] == currentPlayerNumber and gameP4.plate[i][j+3] == currentPlayerNumber):
                isWin = True
            j += 1
        i += 1

    i = 0
    while i < gameP4.size_y and not isWin:
        j = 0
        while j < gameP4.size_x and not isWin:
            if (j >= 3 and i <= 2 and gameP4.plate[i][j] == currentPlayerNumber and gameP4.plate[i+1][j-1] == currentPlayerNumber
                and gameP4.plate[i+2][j-2] == currentPlayerNumber and gameP4.plate[i+3][j-3] == currentPlayerNumber):
                isWin = True
            if (i <= 2 and j <= 5 and gameP4.plate[i][j] == currentPlayerNumber and gameP4.plate[i+1][j+1] == currentPlayerNumber
                and gameP4.plate[i+2][j+2] == currentPlayerNumber and gameP4.plate[i+3][j+3] == currentPlayerNumber):
                isWin = True
            j += 1
        i += 1  
    return isWin


def pointsDistribution(gameP4: GameP4, curPlayer : Player, curPlayers : CurrentPlayers, conn : Connection):
    if checkWin(gameP4,curPlayer):
        print(set_color_green("🙂 Bravo c'est " + "(" + curPlayer.name +")"+ " qui l'emporte"))
        addPoint(curPlayer.id,gameP4.pointWin,conn,gameP4.colName)
        if curPlayer.id == curPlayers.player1.id:
            addPoint(curPlayers.player2.id,gameP4.pointLoose,conn,gameP4.colName)
        else:
            addPoint(curPlayers.player1.id,gameP4.pointLoose,conn,gameP4.colName)
    else:
        print(set_color_green("🙂 Bravo une egalité parfaite "+ curPlayers.player1.name + " et "+ curPlayers.player2.name + " vous remportez " + str(gameP4.pointDraw) + " points"))
        addPoint(curPlayers.player1.id,gameP4.pointDraw,conn,gameP4.colName)
        addPoint(curPlayers.player2.id, gameP4.pointDraw,conn,gameP4.colName)


def checkDraw(gameP4 : GameP4, currPlayer : Player)->bool:
    i : int
    j : int
    isDraw: bool

    isDraw = True
    if checkWin(gameP4,currPlayer):
        return not isDraw
    for i in range(0,gameP4.size_y):
        for j in range(0, gameP4.size_x):
            if gameP4.plate[i][j] == 0:
                isDraw  = False
    return isDraw

def play(gameP4 : GameP4, column :int, number : int)->bool:
    i : int
    canPlay : bool

    canPlay = False
    i = 0
    for i in range(gameP4.size_y - 1 ,-1,-1) :
        if gameP4.plate[i][column-1]  == 0 and not canPlay:
            gameP4.plate[i][column-1] = number
            canPlay = True
    return canPlay

     
    
def displayGrid(gameP4 : GameP4, currentPLayers  : CurrentPlayers)->None:
    i : int
    j : int

    i = 0 
    j = 0
    print("  " ,end="")
    for i in range(0,gameP4.size_x):
        print(set_color_red(str(i+1)), end="    ")
    print()
    for i in range(0,gameP4.size_y):
        print(set_color_blue("+") + set_color_blue("----+")*gameP4.size_x)
        print(set_color_blue("|"),end="")
        for j in range(0,gameP4.size_x):
            if gameP4.plate[i][j] == currentPLayers.player1.playerNumber:
                print(f" {gameP4.player1Pawn}  "+set_color_blue("|"),end="")
            elif gameP4.plate[i][j] == currentPLayers.player2.playerNumber:
                print(f" {gameP4.player2Pawn}  "+set_color_blue("|"),end="")
            else:
                print(f"    "+set_color_blue("|"),end="")
        print()
    print(set_color_blue("+") + set_color_blue("----+")*gameP4.size_x)


def game(currentPlayers : CurrentPlayers, conn : Connection):
    gameP4 : GameP4
    finished : bool
    currentPlayer : Player
    choice : str

    finished = False
    gameP4 = GameP4()
    gameP4Init(gameP4)
    displayStartingMenu()
    print("vous allez joueur sur cette grille")
    displayGrid(gameP4,currentPlayers)
    currentPlayer = currentPlayers.player1
    while not finished:
        print(checkDraw(gameP4,currentPlayer))
        print(set_color_green("("+currentPlayer.name + ")") + " à toi de jouer")
        choice = input("chosi la collonne ou tu souhaites deposer ton pion")
        while not isDigit(choice) or int(choice) <= 0 or int(choice) >= 8 :
            choice = input(set_color_yellow("chosi la collonne ou tu souhaites deposer ton pion entre 1 et 7 inclus"))
        if(not play(gameP4,int(choice),currentPlayer.playerNumber)):
            print(set_color_red(f"⛔ ({currentPlayer.name}) il ne reste plus d'emplacmenent libre sur cette colonne"))
            continue
        displayGrid(gameP4,currentPlayers)
        if checkWin(gameP4,currentPlayer) or checkDraw(gameP4,currentPlayer):
            finished = True
            continue
        currentPlayer = getOtherPlayer(currentPlayers,currentPlayer)
    pointsDistribution(gameP4, currentPlayer, currentPlayers, conn)

"""
#data set de test tout ca est fait dans le main normalement
cp : CurrentPlayers
p1 :Player
p2: Player
p1 = Player()
p2 = Player()

p1.id = 1
p1.name = "Louis"
p1.scoreMatches = 10
p1.scoreP4 = 10
p1.scoreRiddle = 10
p1.scoreTtt  = 10

p2.id = 10
p2.name = "Lorie"
p2.scoreMatches = 10
p2.scoreP4 = 10
p2.scoreRiddle = 10
p2.scoreTtt  = 10
cp = CurrentPlayers()
cp.player1 = p1
cp.player2 = p2
currentPlayersInit(cp,p1,p2)
#game(cp)
gameP4 : GameP4
gameP4 = GameP4()
gameP4Init(gameP4)
con = sqlite3.connect("db.sqlite")
game(cp,con)
"""