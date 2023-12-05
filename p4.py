from entity.gameP4 import GameP4, gameP4Init
from entity.player import CurrentPlayers, Player
from helpers.colors import *
from helpers.inputChecker import isDigit
from entity.winningInformations import *
from sqlite3 import Connection
from helpers.helperPlayer import getOtherPlayer
from helpers.startingMenu import displayStartingMenu
from helpers.pointRepartition import pointsDistribution

def checkWin(gameP4: GameP4, currentPlayer: Player) -> bool:
    """
        Vérifie si le joueur actuel a gagné dans le Puissance 4.

        Cette fonction vérifie si le joueur actuel a gagné dans le jeu Puissance 4 en recherchant des alignements de 4 de ses pions horizontalement, verticalement ou en diagonale.

        Args:
            gameP4 (GameP4): L'instance de la classe GameP4 représentant le jeu en cours.
            currentPlayer (Player): L'instance de la classe Player correspondant au joueur actuel.

        Returns:
            bool: True si le joueur actuel a gagné, False sinon.

    """
    i: int
    j: int
    isWin: bool
    currentPlayerNumber: int

    i = 0
    j = 0
    isWin = False
    currentPlayerNumber = currentPlayer.playerNumber
    # verification verticale
    while i < gameP4.sizeY - 3 and not isWin:
        j = 0
        while j < gameP4.sizeX:
            if (gameP4.plate[i][j] == currentPlayerNumber and gameP4.plate[i+1][j] == currentPlayerNumber
                    and gameP4.plate[i+2][j] == currentPlayerNumber and gameP4.plate[i+3][j] == currentPlayerNumber):
                isWin = True
            j += 1
        i += 1

    i = 0
    # verification horizontale
    while i < gameP4.sizeY and not isWin:
        j = 0
        while j < gameP4.sizeX - 3 and not isWin:
            if (gameP4.plate[i][j] == currentPlayerNumber and gameP4.plate[i][j+1] == currentPlayerNumber
                    and gameP4.plate[i][j+2] == currentPlayerNumber and gameP4.plate[i][j+3] == currentPlayerNumber):
                isWin = True
            j += 1
        i += 1

    i = 0
    # verification des diagonales
    while i < gameP4.sizeY and not isWin:
        j = 0
        while j < gameP4.sizeX and not isWin:
            if (j >= 3 and i <= 2 and gameP4.plate[i][j] == currentPlayerNumber and gameP4.plate[i+1][j-1] == currentPlayerNumber
                    and gameP4.plate[i+2][j-2] == currentPlayerNumber and gameP4.plate[i+3][j-3] == currentPlayerNumber):
                isWin = True
            if (i + 3 < gameP4.sizeY and j + 3 < gameP4.sizeX 
            and gameP4.plate[i][j] == currentPlayerNumber 
            and gameP4.plate[i+1][j+1] == currentPlayerNumber 
            and gameP4.plate[i+2][j+2] == currentPlayerNumber 
            and gameP4.plate[i+3][j+3] == currentPlayerNumber):
                isWin = True
            j += 1
        i += 1
    return isWin




def checkDraw(gameP4: GameP4, currPlayer: Player) -> bool:
    """
        Vérifie s'il y a égalité dans la partie de Puissance 4.

        Cette fonction vérifie s'il y a égalité (match nul) dans la partie de Puissance 4. Il y a égalité si la grille est remplie et qu'aucun joueur n'a gagné.

        Args:
            gameP4 (GameP4): L'instance de la classe GameP4 représentant le jeu en cours.
            currPlayer (Player): L'instance de la classe Player correspondant au joueur actuel.

        Returns:
            bool: True s'il y a égalité, False sinon.
    """
    i: int
    j: int
    isDraw: bool

    isDraw = True
    # on regarde si il y a une victoire car si y a une victoire il n'y a pas de 
    if checkWin(gameP4, currPlayer):
        return not isDraw
    for i in range(0, gameP4.sizeY):
        for j in range(0, gameP4.sizeX):
            if gameP4.plate[i][j] == 0:
                isDraw = False
    return isDraw


def play(gameP4: GameP4, column: int, number: int) -> bool:
    """
        Cette fonction permet à un joueur de jouer un pion dans la colonne spécifiée.

        Args:
            gameP4 (GameP4): L'objet du jeu Puissance 4.
            column (int): La colonne dans laquelle le joueur souhaite jouer.
            number (int): Le numéro du joueur qui effectue le coup.

        Returns:
            bool: True si le coup a été joué avec succès, False sinon.
    """

    i: int
    canPlay: bool

    canPlay = False
    i = 0
    for i in range(gameP4.sizeY - 1, -1, -1):
        #on verifie que la case est libre et que l'on a pas encore joué
        if gameP4.plate[i][column-1] == 0 and not canPlay:
            gameP4.plate[i][column-1] = number
            #on renseigne le fait que l'on a joué
            canPlay = True
    return canPlay


def displayGrid(gameP4: GameP4, currentPLayers: CurrentPlayers) -> None:
    """
        Affiche la grille de jeu du Puissance 4.

        Cette fonction affiche la grille de jeu du Puissance 4, avec les pions des joueurs. Les colonnes et lignes sont numérotées, et les pions des joueurs sont affichés en couleur.

        Args:
            gameP4 (GameP4): L'instance de la classe GameP4 représentant le jeu en cours.
            currentPlayers (CurrentPlayers): L'instance de la classe CurrentPlayers contenant les deux joueurs.

        Returns:
            None
    """
    i: int
    j: int

    i = 0
    j = 0
    # affichage de l'emplacement de chaque colonne
    print("  ", end="")
    for i in range(0, gameP4.sizeX):
        print(setColorRed(str(i+1)), end="    ")
    print()
    for i in range(0, gameP4.sizeY):
        #affichage de la ligne
        print(setColorBlue("+") + setColorBlue("----+")*gameP4.sizeX)
        print(setColorBlue("|"), end="")
        #affichage des cases avec pion si present
        for j in range(0, gameP4.sizeX):
            if gameP4.plate[i][j] == currentPLayers.player1.playerNumber:
                print(f" {gameP4.player1Pawn}  "+setColorBlue("|"), end="")
            elif gameP4.plate[i][j] == currentPLayers.player2.playerNumber:
                print(f" {gameP4.player2Pawn}  "+setColorBlue("|"), end="")
            else:
                print(f"    "+setColorBlue("|"), end="")
        print()
    print(setColorBlue("+") + setColorBlue("----+")*gameP4.sizeX)


def game(currentPlayers: CurrentPlayers, conn: Connection) -> None:
    """
        Gère le déroulement d'une partie de Puissance 4.

        Cette fonction gère le déroulement d'une partie de Puissance 4, y compris l'affichage de la grille, les tours des joueurs, la vérification de la victoire ou de l'égalité, et la distribution des points à la fin de la partie.

        Args:
            currentPlayers (CurrentPlayers): L'instance de la classe CurrentPlayers contenant les deux joueurs.
            conn (Connection): L'objet de connexion à la base de données pour enregistrer les points.

        Returns:
            None
    """
    gameP4: GameP4
    finished: bool
    currentPlayer: Player
    choice: str
    winningInformations : WinningInformations

    finished = False
    gameP4 = GameP4()
    winningInformations = WinningInformations()
    #Initialisation du jeu
    gameP4Init(gameP4)
    displayStartingMenu("Puissance 4", [
        "REGLES DU JEU :",
        "1. A votre tour, insérez l’un de vos pions par le haut dans n’importe quelle colonne de la grille.",
        "2. Jouez ensuite à tour de rôle, jusqu’à ce qu’un joueur parvienne à aligner 4 de ses pions horizontalement, verticalement ou en diagonale. ",
        "3. Le premier joueur à aligner 4 de ses pions a gagné !"
    ])
    print("vous allez joueur sur cette grille")
    displayGrid(gameP4, currentPlayers)
    currentPlayer = currentPlayers.player1
    while not finished:
        print(setColorGreen("("+currentPlayer.name + ")") + " à toi de jouer")
        choice = input("choisi la collonne ou tu souhaites deposer ton pion")
        while not isDigit(choice) or int(choice) <= 0 or int(choice) >= 8:
            choice = input(setColorYellow(
                "choisi la collonne ou tu souhaites deposer ton pion entre 1 et 7 inclus"))
        if (not play(gameP4, int(choice), currentPlayer.playerNumber)):
            print(setColorRed(
                f"⛔ ({currentPlayer.name}) il ne reste plus d'emplacmenent libre sur cette colonne"))
        else:
            displayGrid(gameP4, currentPlayers)
            if checkWin(gameP4, currentPlayer) or checkDraw(gameP4, currentPlayer):
                finished = True
            else:
                #recuperation du joueur suivant
                currentPlayer = getOtherPlayer(currentPlayers, currentPlayer)
    winningInformationsInit(winningInformations, gameP4.colName,gameP4.pointDraw,gameP4.pointWin,gameP4.pointLoose,checkDraw(gameP4,currentPlayer))
    pointsDistribution(winningInformations,currentPlayers,currentPlayer,conn)
