
from helpers.colors import *
from entity.player import *
from entity.gameTicTacToe import *
from sqlite3 import Connection
from helpers.inputChecker import isDigit
from helpers.helperPlayer import getOtherPlayer
from helpers.startingMenu import displayStartingMenu
from helpers.pointRepartition import pointsDistribution
from entity.winningInformations import *


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
    #affichage de l'emplacement des case en x
    print("    ", end="")
    for j in range(gameTicTacToe.sizeY): 
        print(str(j + 1) + "   ", end="")
    print()
    for i in range(0,gameTicTacToe.sizeY):
        print("  +" + "---+"*gameTicTacToe.sizeX)
        print(str(i+1)+" |",end="")
        #affichage de la cage avec un pion si present
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
    #verification horizontale
    while i < gameTicTacToe.sizeY  and not isWin:
        if (gameTicTacToe.plate[i][0] == currentPlayerNumber and gameTicTacToe.plate[i][1] == currentPlayerNumber and  gameTicTacToe.plate[i][2] == currentPlayerNumber):
            isWin = True
        i += 1
    i = 0
    #verification verticale
    while i < gameTicTacToe.sizeX  and not isWin:
        if (gameTicTacToe.plate[0][i] == currentPlayerNumber and gameTicTacToe.plate[1][i] == currentPlayerNumber and  gameTicTacToe.plate[2][i] == currentPlayerNumber):
            isWin = True
        i += 1
    i = 0
    #verification des diagonales
    if ((gameTicTacToe.plate[0][0] == currentPlayerNumber and gameTicTacToe.plate[1][1] == currentPlayerNumber and  gameTicTacToe.plate[2][2] == currentPlayerNumber) or (gameTicTacToe.plate[0][2] == currentPlayerNumber and gameTicTacToe.plate[1][1] == currentPlayerNumber and  gameTicTacToe.plate[2][0] == currentPlayerNumber)):
        isWin = True
    return isWin


def checkDraw(gameTicTacToe : GameTicTacToe, currentPlayer : Player)->bool:
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
    #on verifie si le joueur n'a pas gagné car si c'est le cas il n'y a pas d'égalité
    if checkWin(gameTicTacToe,currentPlayer):
        isDraw = False
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
    canPlay : bool

    canPlay = False
    #on verifie  que la case comporte bien un 0 si c'est le cas cela veut dire qu'elle est libre
    if gameTicTacToe.plate[choiceY -1][choiceX -1] == 0:
        gameTicTacToe.plate[choiceY -1][choiceX -1] = currentPlayer.playerNumber
        canPlay = True
    #retourne si le joueur a pu jouer
    return canPlay


def game(currentPlayers : CurrentPlayers, conn : Connection)->None:
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
    winningInformations : WinningInformations
    finished : bool
    currentPlayer : Player
    choiceX : str
    choiceY : str

    finished = False
    gameTicTacToe = GameTicTacToe()
    winningInformations = WinningInformations()
    #initialisation du jeu
    gameTicTacToeInit(gameTicTacToe)
    displayStartingMenu("Morpion",[
        "REGLES DU JEU :",
        "1. À chaque joueur sera affecté une jeton ",
        "2. Les joueurs placent à tour de rôle un jeton sur une case du quadrillage. ",
        "3. Le gagnant est celui qui parvient à aligner 3 jetons identiques horizontalement verticalement ou en diagonale. ",
        "4. AA chaque joueur sera affecté une jeton"
    ])
    print("vous allez joueur sur cette grille")
    displayGrid(gameTicTacToe,currentPlayers)
    currentPlayer = currentPlayers.player1
    while not finished:
        print(setColorGreen("("+ currentPlayer.name + ")") + " à toi de jouer")
        choiceX = input("choisi ou tu souhaites deposer ton pion sur l'axe x (ligne) ")
        while not isDigit(choiceX) or int(choiceX) <= 0 or int(choiceX) >= 4 :
            choiceX = input(setColorYellow("chosi sur l'axe x (ligne) ou tu souhaites deposer ton pion entre 1 et 3 inclus "))
        choiceY = input("choisi ou tu souhaites deposer ton pion l'axe y (colonne) ")
        while not isDigit(choiceY) or int(choiceY) <= 0 or int(choiceY) >= 4 :
            choiceY = input(setColorYellow("chosi l'axe y (colonne) ou tu souhaites deposer ton pion entre 1 et 3 inclus "))
        #si le joueur n'a pas pu jouer c'est que la case est déjà occupée
        if(not play(gameTicTacToe,currentPlayer,int(choiceX),int(choiceY))):
            print(setColorRed(f"⛔({currentPlayer.name}) il ne reste plus d'emplacmenent libre sur cette colonne"))
        else:
            displayGrid(gameTicTacToe, currentPlayers)
            print(checkWin(gameTicTacToe,currentPlayer))
            #si il y a une victoire ou une égalité on arrete le jeu 
            if checkWin(gameTicTacToe,currentPlayer) or checkDraw(gameTicTacToe,currentPlayer):
                finished = True
            else:
                currentPlayer = getOtherPlayer(currentPlayers,currentPlayer)
    winningInformationsInit(winningInformations, gameTicTacToe.colName,gameTicTacToe.pointDraw,gameTicTacToe.pointWin,gameTicTacToe.pointLoose,checkDraw(gameTicTacToe,currentPlayer))
    pointsDistribution(winningInformations,currentPlayers,currentPlayer,conn)    
