
from helpers.colors import *
from entity.player import *
from entity.gameTicTacToe import *
from sqlite3 import Connection
from helpers.inputChecker import isDigit
from helperPlayer import getOtherPlayer
from dataServices.sqlCommands import addPoint

def displayStartingMenu():
    """
        Affiche le menu de démarrage du jeu du Morpion.

        Cette fonction affiche un menu de démarrage du jeu du Morpion, y compris les règles du jeu et un message de chargement.

        Args:
            Aucun.

        Returns:
            None
    """
    print(setColorGreen("Bienvenue à vous dans le jeu du Morpion"))
    print(setColorGreen("REGLES DU JEU \n 1. À chaque joueur sera affecté une jeton \n 2. Les joueurs placent à tour de rôle un jeton sur une case du quadrillage. \n 3. Le gagnant est celui qui parvient à aligner 3 jetons identiques horizontalement verticalement ou en diagonale. \n 4. AA chaque joueur sera affecté une jeton"))
    print(setColorGreen("Chargement..."))

def displayGrid(gameTicTacToe : GameTicTacToe, currentPLayers : CurrentPlayers)->None:
    """
        Affiche le plateau de jeu du Morpion.

        Cette fonction affiche le plateau de jeu du Morpion, y compris les positions des jetons des joueurs actuels.

        Args:
            gameTicTacToe (GameTicTacToe): L'instance de la classe GameTicTacToe représentant le jeu.
            currentPLayers (CurrentPlayers): L'instance de la classe CurrentPlayers contenant les joueurs actuels.

        Returns:
            None
    """
    i : int
    j : int

    i = 0 
    j = 0
    print("    ", end="")
    for j in range(gameTicTacToe.sizeY): 
        print(str(j + 1) + "   ", end="")
    print()
    for i in range(0,gameTicTacToe.sizeY):
        print("  +" + "---+"*gameTicTacToe.sizeX)
        print(str(i+1)+" |",end="")
        for j in range(0,gameTicTacToe.sizeX):
            if gameTicTacToe.plate[i][j] == currentPLayers.player1.playerNumber:
                print(f" {gameTicTacToe.player1Pawn} |",end="")
            elif gameTicTacToe.plate[i][j] == currentPLayers.player2.playerNumber:
                print(f" {gameTicTacToe.player2Pawn} |",end="")
            else:
                print(f"   |",end="")
        print()
    print("  +" + "---+"*gameTicTacToe.sizeX)

def checkWin(gameTicTacToe : GameTicTacToe, currentPlayer : Player)->bool:
    """
        Vérifie si le joueur actuel a remporté la partie.

        Cette fonction vérifie si le joueur actuel a gagné la partie en vérifiant les lignes, les colonnes et les diagonales du plateau de jeu.

        Args:
            gameTicTacToe (GameTicTacToe): L'instance de la classe GameTicTacToe représentant le jeu.
            currentPlayer (Player): L'instance de la classe Player correspondant au joueur actuel.

        Returns:
            bool: True si le joueur actuel a gagné, False sinon.
    """
    i : int
    isWin : bool
    currentPlayerNumber : int

    i = 0
  
    isWin = False
    currentPlayerNumber = currentPlayer.playerNumber

    while i < gameTicTacToe.sizeY  and not isWin:
        if (gameTicTacToe.plate[i][0] == currentPlayerNumber and gameTicTacToe.plate[i][1] == currentPlayerNumber and  gameTicTacToe.plate[i][2] == currentPlayerNumber):
            isWin = True
        i += 1
    i = 0
    while i < gameTicTacToe.sizeX  and not isWin:
        if (gameTicTacToe.plate[0][i] == currentPlayerNumber and gameTicTacToe.plate[1][i] == currentPlayerNumber and  gameTicTacToe.plate[2][i] == currentPlayerNumber):
            isWin = True
        i += 1
    i = 0
    if ((gameTicTacToe.plate[0][0] == currentPlayerNumber and gameTicTacToe.plate[1][1] == currentPlayerNumber and  gameTicTacToe.plate[2][2]) or (gameTicTacToe.plate[0][2] == currentPlayerNumber and gameTicTacToe.plate[1][1] == currentPlayerNumber and  gameTicTacToe.plate[2][0])):
        isWin = True
    return isWin


def checkDraw(gameTicTacToe : GameTicTacToe):
    """
        Vérifie si la partie est un match nul (matche null).

        Cette fonction vérifie si la partie est un match nul en parcourant le plateau de jeu pour rechercher des cases vides.

        Args:
            gameTicTacToe (GameTicTacToe): L'instance de la classe GameTicTacToe représentant le jeu.

        Returns:
            bool: True si la partie est un match nul, False sinon
    """
    i : int
    j : int
    isDraw : bool

    i = 0
    j = 0
    isDraw = True
    
    while i <  gameTicTacToe.sizeY and isDraw:
        while j < gameTicTacToe.sizeX and isDraw:
            if gameTicTacToe.plate[i][j] == 0 :
                isDraw = False
            j+=1
        i+=1
        j = 0
    return isDraw

def play(gameTicTacToe : GameTicTacToe,currentPlayer : Player, choiceX:int,choiceY:int)->bool:
    """
        Joue un coup sur le plateau de jeu.

        Cette fonction permet à un joueur de jouer un coup sur le plateau de jeu en plaçant son jeton à la position spécifiée.

        Args:
            gameTicTacToe (GameTicTacToe): L'instance de la classe GameTicTacToe représentant le jeu.
            currentPlayer (Player): L'instance de la classe Player correspondant au joueur actuel.
            choiceX (int): La coordonnée X de la position choisie par le joueur.
            choiceY (int): La coordonnée Y de la position choisie par le joueur.

        Returns:
            bool: True si le coup a été joué avec succès (la case était vide), False sinon.

    """
    if gameTicTacToe.plate[choiceY -1][choiceX -1] == 0:
        gameTicTacToe.plate[choiceY -1][choiceX -1] = currentPlayer.playerNumber
        return True
    return False

def pointsDistribution(gameTicTacToe: GameTicTacToe, curPlayer : Player, curPlayers : CurrentPlayers, conn : Connection):
    """
        Distribue les points en fonction du résultat de la partie.

        Cette fonction distribue les points aux joueurs en fonction du résultat de la partie (victoire ou match nul).

        Args:
            gameTicTacToe (GameTicTacToe): L'instance de la classe GameTicTacToe représentant le jeu.
            curPlayer (Player): L'instance de la classe Player correspondant au joueur actuel.
            curPlayers (CurrentPlayers): L'instance de la classe CurrentPlayers contenant les joueurs actuels.
            conn (Connection): L'objet de connexion à la base de données pour enregistrer les points.

        Returns:
            None
    """
    if checkWin(gameTicTacToe,curPlayer):
        print(setColorGreen("🙂 Bravo c'est " + "(" + curPlayer.name +")"+ " qui l'emporte"))
        addPoint(curPlayer.id,gameTicTacToe.pointWin,conn,gameTicTacToe.colName)
        if curPlayer.id == curPlayers.player1.id:
            addPoint(curPlayers.player2.id,gameTicTacToe.pointLoose,conn,gameTicTacToe.colName)
        else:
            addPoint(curPlayers.player1.id,gameTicTacToe.pointLoose,conn,gameTicTacToe.colName)
    else:
        print(setColorGreen("🙂 Bravo une egalité parfaite "+ curPlayers.player1.name + " et "+ curPlayers.player2.name + " vous remportez " + str(gameTicTacToe.pointDraw) + " points"))
        addPoint(curPlayers.player1.id,gameTicTacToe.pointDraw,conn,gameTicTacToe.colName)
        addPoint(curPlayers.player2.id, gameTicTacToe.pointDraw,conn,gameTicTacToe.colName)

def game(currentPlayers : CurrentPlayers, conn : Connection):
    """
        Déroule le jeu du Morpion entre deux joueurs.

        Cette fonction gère le déroulement du jeu du Morpion entre deux joueurs. Elle initialise le plateau de jeu, affiche le menu de démarrage,
        permet aux joueurs de jouer tour à tour, vérifie s'ils ont gagné ou si la partie est un match nul, puis distribue les points en conséquence.

        Args:
            currentPlayers (CurrentPlayers): L'instance de la classe CurrentPlayers contenant les deux joueurs.
            conn (Connection): L'objet de connexion à la base de données pour enregistrer les points.

        Returns:
            None
    """
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
        print(setColorGreen("("+ currentPlayer.name + ")") + " à toi de jouer")
        choiceX = input("choisi ou tu souhaites deposer ton pion sur l'axe x")
        while not isDigit(choiceX) or int(choiceX) <= 0 or int(choiceX) >= 4 :
            choiceX = input(setColorYellow("chosi sur l'axe x ou tu souhaites deposer ton pion entre 1 et 3 inclus"))
        choiceY = input("choisi ou tu souhaites deposer ton pion l'axe y")
        while not isDigit(choiceY) or int(choiceY) <= 0 or int(choiceY) >= 4 :
            choiceY = input(setColorYellow("chosi l'axe y ou tu souhaites deposer ton pion entre 1 et 3 inclus"))
        if(not play(gameTicTacToe,currentPlayer,int(choiceX),int(choiceY))):
            print(setColorRed(f"⛔ ({currentPlayer.name}) il ne reste plus d'emplacmenent libre sur cette colonne"))
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