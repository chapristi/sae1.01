from entity.gameP4 import GameP4, gameP4Init
from entity.player import CurrentPlayers, Player,configureBotsLevel
from helpers.colors import *
from helpers.inputChecker import isDigit
from entity.winningInformations import *
from sqlite3 import Connection
from helpers.helperPlayer import getOtherPlayer
from helpers.startingMenu import displayStartingMenu
from helpers.pointRepartition import pointsDistribution
from random import randint
import time

def remainingMoves(gameP4: GameP4) -> list[tuple[int, int]]:
    """
        Cette fonction détermine les mouvements possibles restants dans le jeu Puissance 4.

        Paramètre :
            - gameP4 (GameP4) : L'instance du jeu Puissance 4.

        Sortie :
            - moves (list[tuple[int, int]]) : Une liste de tuples représentant les coordonnées des emplacements
            où un jeton peut être placé dans le jeu.
    """

    moves  : list[tuple[int,int]]
    isColFinished : bool
    i : int
    j : int
   
    moves = []
    for j in range(gameP4.sizeX):
        i = gameP4.sizeY - 1
        isColFinished = False
        while i >= 0 and not isColFinished:
            # si la case contient 0 c'est qu'elle est libre
            if gameP4.plate[i][j] == 0:
                moves.append((i, j))
                isColFinished = True
            i -= 1

    return moves

   

def alignInTwo(gameP4: GameP4, player : Player) -> int:
    """
        Cette fonction compte le nombre d'alignements potentiels de deux jetons consécutifs pour un joueur spécifié
        dans le jeu Tic Tac Toe.

        Paramètres :
            - gameP4 (GameP4) : L'instance du jeu Tic Tac Toe.
            - player (Player) : Le joueur dont les alignements potentiels sont comptés.

        Sortie :
            - count (int) : Le nombre d'alignements potentiels de deux jetons consécutifs.
    """
    count: int
    i : int
    j : int

    count = 0

    # Vérification horizontale
    for i in range(gameP4.sizeY):
        for j in range(gameP4.sizeX - 1):
            if gameP4.plate[i][j] == player.playerNumber and gameP4.plate[i][j + 1] == player.playerNumber:
                count += 1

    # Vérification verticale
    for i in range(gameP4.sizeY - 1):
        for j in range(gameP4.sizeX):
            if gameP4.plate[i][j] == player.playerNumber and  gameP4.plate[i + 1][j] == player.playerNumber:
                count += 1

    # Vérification diagonale (/)
    for i in range(gameP4.sizeY - 1):
        for j in range(gameP4.sizeX - 1):
            if gameP4.plate[i][j] == player.playerNumber and  gameP4.plate[i + 1][j + 1] == player.playerNumber:
                count += 1

    # Vérification diagonale (\)
    for i in range(1, gameP4.sizeY):
        for j in range(gameP4.sizeX - 1):
            if gameP4.plate[i][j] == player.playerNumber and  gameP4.plate[i - 1][j + 1] == player.playerNumber:
                count += 1

    return count


def alignInThree(gameP4 : GameP4,player : Player):
    """
        Cette fonction compte le nombre d'alignements potentiels de trois jetons consécutifs pour un joueur spécifié
        dans le jeu Tic Tac Toe.

        Paramètres :
            - gameP4 (GameP4) : L'instance du jeu Tic Tac Toe.
            - player (Player) : Le joueur dont les alignements potentiels sont comptés.

        Sortie :
            - count (int) : Le nombre d'alignements potentiels de trois jetons consécutifs.
    """
    count : int
    i: int
    j : int

    count = 0
    # Vérification horizontale
    for i in range(gameP4.sizeY):
        for j in range(gameP4.sizeX - 2):
            if gameP4.plate[i][j] == player.playerNumber and  gameP4.plate[i][j + 1] == player.playerNumber and  gameP4.plate[i][j + 2] == player.playerNumber:
                count += 1

    # Vérification verticale
    for i in range(gameP4.sizeY - 2):
        for j in range(gameP4.sizeX):
            if gameP4.plate[i][j] == player.playerNumber and gameP4.plate[i + 1][j] == player.playerNumber and  gameP4.plate[i + 2][j] == player.playerNumber:
                count += 1

    # Vérification diagonale (/)
    for i in range(gameP4.sizeY - 2):
        for j in range(gameP4.sizeX - 2):
            if gameP4.plate[i][j] == player.playerNumber and  gameP4.plate[i + 1][j + 1] == player.playerNumber and  gameP4.plate[i + 2][j + 2] == player.playerNumber:
                count += 1

    # Vérification diagonale (\)
    for i in range(1, gameP4.sizeY - 1):
        for j in range(gameP4.sizeX - 2):
            if gameP4.plate[i][j] ==  player.playerNumber and gameP4.plate[i - 1][j + 1] ==  player.playerNumber and gameP4.plate[i - 2][j + 2] == player.playerNumber:
                count += 1

    return count   

def scoreAlignement(gameP4 : GameP4,player : Player) -> int:
    """
        Cette fonction attribue un score total basé sur le nombre d'alignements potentiels de deux et trois jetons consécutifs
        pour un joueur spécifié dans le jeu Tic Tac Toe.

        Paramètres :
            - gameP4 (GameP4) : L'instance du jeu Tic Tac Toe.
            - player (Player) : Le joueur dont les alignements potentiels sont pris en compte.

        Sortie :
            - score (int) : Le score total attribué en fonction du nombre d'alignements potentiels.
    """
    scoreAlignementTwo : int
    scoreAlignementThree : int


    scoreAlignementTwo = 1
    scoreAlignementThree = 3

    return  alignInTwo(gameP4, player) * scoreAlignementTwo +  alignInThree(gameP4, player)  * scoreAlignementThree

def evaluateBoard(gameP4 : GameP4, currentPlayers : CurrentPlayers):
    """
        Cette fonction heuristique évalue le plateau de jeu Tic Tac Toe et attribue un score en fonction de la disposition des pions.

        Paramètres :
            - gameP4 (GameP4) : L'instance du jeu Tic Tac Toe.
            - currentPlayers (CurrentPlayers) : Les joueurs actuels du jeu.
            - isPlayer2 (bool) : Un indicateur indiquant si on évalue le plateau du point de vue du joueur 2.

        Sortie :
            - result (int) : Le score attribué au plateau en fonction de la disposition des pions.
    """
    weight : list[list[int]]
    i : int
    j : int
    result : int

    # on fixe le poids de chaques cases
    weight = [
        [3, 4, 5, 7, 5, 4, 3],
        [4, 6, 8, 10, 8, 6, 4],
        [5, 8, 11, 13, 11, 8, 5],
        [5, 8, 11, 13, 11, 8, 5],
        [4, 6, 8, 10, 8, 6, 4],
        [3, 4, 5, 7, 5, 4, 3]
    ]
    result = 0

    for i in range(0,gameP4.sizeY):
        for j in range(0,gameP4.sizeX):
            if gameP4.plate[i][j] == currentPlayers.player2.playerNumber:
                result +=  weight[i][j]
            elif gameP4.plate[i][j] == currentPlayers.player1.playerNumber:
                result -=  weight[i][j]

    #essayer de voir les allignements de trois prions, deux pions et donner des scores en fonction
 
    result += scoreAlignement(gameP4,currentPlayers.player2)
    result -= scoreAlignement(gameP4,currentPlayers.player1)
    return result
    

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

def minimax(gameP4: GameP4, currentPlayers: CurrentPlayers, currentPlayer: Player, depth: int, isMaximizing: bool,alpha : float, beta : float) -> int:
    """
        Implémente l'algorithme Minimax avec élagage alpha-bêta pour le jeu Puissance 4.

        Args :
            - gameP4 (GameP4) : L'instance du jeu Puissance 4.
            - currentPlayers (CurrentPlayers) : Les joueurs actuels du jeu.
            - currentPlayer (Player) : Le joueur pour lequel l'algorithme est en train d'évaluer les mouvements.
            - depth (int) : La profondeur maximale de recherche dans l'arbre de jeu.
            - isMaximizing (bool) : Indique si l'algorithme doit maximiser ou minimiser le score.
            - alpha (float) : La valeur de l'alpha dans l'élagage alpha-bêta.
            - beta (float) : La valeur du bêta dans l'élagage alpha-bêta.

        Returns :
        - int : Le score évalué pour le mouvement optimal dans la situation actuelle.
    """
    move : tuple[int,int]
    eval : int
    min_eval : int
    max_eval : int

    if checkWin(gameP4, currentPlayers.player2):
        return 10000
    elif checkWin(gameP4, currentPlayers.player1):
        return -10000
    elif checkDraw(gameP4, currentPlayers.player2) or checkDraw(gameP4, currentPlayers.player1):
        return 0
    # si on atteint la profondeur max alors on utilise la fonction heuristique pour évaluer le plateau
    elif depth == 0:
        return evaluateBoard(gameP4,currentPlayers)

    if isMaximizing:
        max_eval = -1000000
        for move in remainingMoves(gameP4):
            gameP4.plate[move[0]][move[1]] = currentPlayers.player2.playerNumber
            eval = minimax(gameP4, currentPlayers, currentPlayer, depth - 1, not isMaximizing ,alpha,beta)
            gameP4.plate[move[0]][move[1]] = 0
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = 1000000
        for move in remainingMoves(gameP4):
            gameP4.plate[move[0]][move[1]] = currentPlayers.player1.playerNumber
            eval = minimax(gameP4, currentPlayers, currentPlayer, depth - 1, not isMaximizing ,alpha,beta)
            gameP4.plate[move[0]][move[1]] = 0
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def botRandomPlay(gameP4 : GameP4, currentPlayer :Player) -> None:
    """
        Cette fonction permet à un bot de jouer de manière aléatoire dans le jeu Puissance 4.

        Args :
            - gameP4 (GameP4) : L'instance du jeu Puissance 4.
            - currentPlayer (Player) : Le joueur actuel, qui est un bot.

    """
    el : int
    nbEls : int 
    moves: list[tuple[int,int]]
    move : tuple[int,int]

    moves  = remainingMoves(gameP4)
    nbEls = len(moves)
    # s'il y a au moins un coup à jouer on le joue
    if nbEls > 1 : 
        el = randint(0, nbEls -1)
        move = moves[el] 
        gameP4.plate[move[0]][move[1]] = currentPlayer.playerNumber
        

def bestMove(gameP4: GameP4, currentPlayers: CurrentPlayers,currentPlayer : Player, depth : int) -> None:
    """
        Choisi le meilleur coup possible pour un joueur en utilisant l'algorithme Minimax avec élagage alpha-bêta.

        Paramètres :
            - gameP4 (GameP4) : L'instance du jeu Puissance 4.
            - currentPlayers (CurrentPlayers) : Les joueurs actuels du jeu.
            - currentPlayer (Player) : Le joueur actuel pour lequel le meilleur coup doit être déterminé.
            - depth (int) : La profondeur maximale de recherche dans l'arbre de jeu.
    """
    eval: int
    bestEval : int
    bestMove : tuple[int,int]
    
    bestMove = remainingMoves(gameP4)[0]
    # on donne un score qui sera dépacé afin d'attribuer une valeur de départ
    bestEval = -1000000 if currentPlayer == currentPlayers.player2 else 1000000
    for move in remainingMoves(gameP4):
        # choix de la case
        gameP4.plate[move[0]][move[1]] = currentPlayer.playerNumber
        # la fonction minimax nous renvoie un score pour la case
        eval = minimax(gameP4, currentPlayers,currentPlayer, depth, currentPlayer == currentPlayers.player1,float("-inf"),float("inf"))
        # reinitialisation de la case
        gameP4.plate[move[0]][move[1]] = 0
        if (currentPlayer == currentPlayers.player2 and eval > bestEval) or (currentPlayer == currentPlayers.player1 and eval < bestEval):
            bestEval = eval
            bestMove = move

    gameP4.plate[bestMove[0]][bestMove[1]] = currentPlayer.playerNumber

def botLevel2Play(gameP4: GameP4, currentPlayers: CurrentPlayers,currentPlayer : Player) -> None:
    """
        Cette fonction permet à un bot de jouer au Puissance 4 avec différents niveaux de difficulté.
        
        Paramètres :
            - gameP4 (GameP4) : L'instance du jeu Puissance 4.
            - currentPlayers (CurrentPlayers) : Les joueurs actuels du jeu.
            - currentPlayer (Player) : Le joueur actuel, qui peut être un bot ou un joueur humain.
        return  : rien
    """
    # si le joueur est bien un bot
    if currentPlayer.isBot:
        if currentPlayer.lvl == 1:
            botRandomPlay(gameP4,currentPlayer)
        elif currentPlayer.lvl == 2:
            bestMove(gameP4,currentPlayers,currentPlayer,1)
        elif currentPlayer.lvl == 3:
            bestMove(gameP4,currentPlayers,currentPlayer,2)
        elif currentPlayer.lvl == 4:
            bestMove(gameP4,currentPlayers,currentPlayer,3)
        elif currentPlayer.lvl == 5:
            bestMove(gameP4,currentPlayers,currentPlayer,6)
        else:
            print("un problème est survenue")
    
    
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
    configureBotsLevel(currentPlayers)
    print("vous allez joueur sur cette grille")
    displayGrid(gameP4, currentPlayers)
    currentPlayer = currentPlayers.player1
    while not finished:
        print(setColorGreen("("+currentPlayer.name + ")") + " à toi de jouer")
        # si le joueur est un bot
        if currentPlayer.isBot:
            # on demande à l'utilisateur s'il veu changer le niveau du bot
            botLevel2Play(gameP4,currentPlayers,currentPlayer)
            time.sleep(1)
            displayGrid(gameP4, currentPlayers)
            if checkWin(gameP4, currentPlayer) or checkDraw(gameP4, currentPlayer):
                finished = True
            else:
                #recuperation du joueur suivant
                currentPlayer = getOtherPlayer(currentPlayers, currentPlayer)
        else:
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
            print(remainingMoves(gameP4))

    winningInformationsInit(winningInformations, gameP4.colName,gameP4.pointDraw,gameP4.pointWin,gameP4.pointLoose,checkDraw(gameP4,currentPlayer))
    pointsDistribution(winningInformations,currentPlayers,currentPlayer,conn)
