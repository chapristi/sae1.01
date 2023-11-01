
from colors import *
from player import *
from gameTicTacToe import *
from sqlite3 import Connection
from input_checker import isDigit
from helperPlayer import getOtherPlayer
from sql_commands import addPoint

def displayStartingMenu():
    print(set_color_green("Bienvenue à vous dans le jeu du Morpion"))
    print(set_color_green("Chargement..."))

def displayGrid(gameTicTacToe : GameTicTacToe, currentPLayers : CurrentPlayers)->None:
    i : int
    j : int

    i = 0 
    j = 0
    print("    ", end="")
    for j in range(gameTicTacToe.size_y): 
        print(str(j + 1) + "   ", end="")
    print()
    for i in range(0,gameTicTacToe.size_y):
        print("  +" + "---+"*gameTicTacToe.size_x)
        print(str(i+1)+" |",end="")
        for j in range(0,gameTicTacToe.size_x):
            if gameTicTacToe.plate[i][j] == currentPLayers.player1.playerNumber:
                print(f" {gameTicTacToe.player1Pawn} |",end="")
            elif gameTicTacToe.plate[i][j] == currentPLayers.player2.playerNumber:
                print(f" {gameTicTacToe.player2Pawn} |",end="")
            else:
                print(f"   |",end="")
        print()
    print("  +" + "---+"*gameTicTacToe.size_x)

def checkWin(gameTicTacToe : GameTicTacToe, currentPlayer : Player)->bool:
    i : int
    isWin : bool
    currentPlayerNumber : int

    i = 0
  
    isWin = False
    currentPlayerNumber = currentPlayer.playerNumber

    while i < gameTicTacToe.size_y  and not isWin:
        if (gameTicTacToe.plate[i][0] == currentPlayerNumber and gameTicTacToe.plate[i][1] == currentPlayerNumber and  gameTicTacToe.plate[i][2] == currentPlayerNumber):
            isWin = True
        i += 1
    i = 0
    while i < gameTicTacToe.size_x  and not isWin:
        if (gameTicTacToe.plate[0][i] == currentPlayerNumber and gameTicTacToe.plate[1][i] == currentPlayerNumber and  gameTicTacToe.plate[2][i] == currentPlayerNumber):
            isWin = True
        i += 1
    i = 0
    if ((gameTicTacToe.plate[0][0] == currentPlayerNumber and gameTicTacToe.plate[1][1] == currentPlayerNumber and  gameTicTacToe.plate[2][2]) or (gameTicTacToe.plate[0][2] == currentPlayerNumber and gameTicTacToe.plate[1][1] == currentPlayerNumber and  gameTicTacToe.plate[2][0])):
        isWin = True
    return isWin
def checkDraw(gameTicTacToe : GameTicTacToe):
    i : int
    j : int
    isDraw : bool

    i = 0
    j = 0
    isDraw = True
    while i <  gameTicTacToe.size_y and isDraw:
        while j < gameTicTacToe.size_x and isDraw:
            if gameTicTacToe.plate[i][j] == 0 :
                isDraw = False
            j+=1
        i+=1
        j = 0
    return isDraw

def play(gameTicTacToe : GameTicTacToe,currentPlayer : Player, choiceX:int,choiceY:int)->bool:
    if gameTicTacToe.plate[choiceY -1][choiceX -1] == 0:
        gameTicTacToe.plate[choiceY -1][choiceX -1] = currentPlayer.playerNumber
        return True
    return False

def pointsDistribution(gameTicTacToe: GameTicTacToe, curPlayer : Player, curPlayers : CurrentPlayers, conn : Connection):
    if checkWin(gameTicTacToe,curPlayer):
        print(set_color_green("🙂 Bravo c'est " + "(" + curPlayer.name +")"+ " qui l'emporte"))
        addPoint(curPlayer.id,gameTicTacToe.pointWin,conn,gameTicTacToe.colName)
        if curPlayer.id == curPlayers.player1.id:
            addPoint(curPlayers.player2.id,gameTicTacToe.pointLoose,conn,gameTicTacToe.colName)
        else:
            addPoint(curPlayers.player1.id,gameTicTacToe.pointLoose,conn,gameTicTacToe.colName)
    else:
        print(set_color_green("🙂 Bravo une egalité parfaite "+ curPlayers.player1.name + " et "+ curPlayers.player2.name + " vous remportez " + str(gameTicTacToe.pointDraw) + " points"))
        addPoint(curPlayers.player1.id,gameTicTacToe.pointDraw,conn,gameTicTacToe.colName)
        addPoint(curPlayers.player2.id, gameTicTacToe.pointDraw,conn,gameTicTacToe.colName)

def game(currentPlayers : CurrentPlayers, conn : Connection):
    gameTicTacToe : GameTicTacToe
    finished : bool
    currentPlayer : Player
    choiceX : str
    choiceY : str

    finished = False
    gameTicTacToe = GameTicTacToe()
    gameTicTacToeInit(gameTicTacToe)
    displayStartingMenu()
    print("vous allez joueur sur cette grille")
    displayGrid(gameTicTacToe,currentPlayers)
    currentPlayer = currentPlayers.player1
    while not finished:
        print(set_color_green("("+ currentPlayer.name + ")") + " à toi de jouer")
        choiceX = input("choisi ou tu souhaites deposer ton pion sur l'axe x")
        while not isDigit(choiceX) or int(choiceX) <= 0 or int(choiceX) >= 4 :
            choiceX = input(set_color_yellow("chosi sur l'axe x ou tu souhaites deposer ton pion entre 1 et 3 inclus"))
        choiceY = input("choisi ou tu souhaites deposer ton pion l'axe y")
        while not isDigit(choiceY) or int(choiceY) <= 0 or int(choiceY) >= 4 :
            choiceY = input(set_color_yellow("chosi l'axe y ou tu souhaites deposer ton pion entre 1 et 3 inclus"))
        if(not play(gameTicTacToe,currentPlayer,int(choiceX),int(choiceY))):
            print(set_color_red(f"⛔ ({currentPlayer.name}) il ne reste plus d'emplacmenent libre sur cette colonne"))
            continue
        displayGrid(gameTicTacToe, currentPlayers)
        if checkWin(gameTicTacToe,currentPlayer) or checkDraw(gameTicTacToe):
            finished = True
            continue
        currentPlayer = getOtherPlayer(currentPlayers,currentPlayer)
    pointsDistribution(gameTicTacToe, currentPlayer, currentPlayers, conn)
    

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
p2.name = "Lorois"
p2.scoreMatches = 10
p2.scoreP4 = 10
p2.scoreRiddle = 10
p2.scoreTtt  = 10
cp = CurrentPlayers()
cp.player1 = p1
cp.player2 = p2
currentPlayersInit(cp,p1,p2)
#game(cp)
con = sqlite3.connect("db.sqlite")
game(cp,con)
"""