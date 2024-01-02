
from helpers.colors import *
from entity.player import *
from entity.gameTicTacToe import *
from sqlite3 import Connection
from helpers.inputChecker import isDigit
from helpers.helperPlayer import getOtherPlayer
from helpers.startingMenu import displayStartingMenu
from helpers.pointRepartition import pointsDistribution
from entity.winningInformations import *
from random import randint
import time

def evaluateBoard(gameTicTacToe : GameTicTacToe, currentPLayers : CurrentPlayers, player2 : bool):
    """
        Évalue le plateau de jeu Tic Tac Toe et attribue un score en fonction de la disposition des pions.

        Args :
            - gameTicTacToe (GameTicTacToe) : L'instance du jeu Tic Tac Toe.
            - currentPlayers (CurrentPlayers) : Les joueurs actuels du jeu.
            - player2 (bool) : Un indicateur indiquant si on évalue le plateau du point de vue du joueur 2.

        Returns :
            - result (int) : Le score attribué au plateau en fonction de la disposition des pions.
    """

    weight : list[list[int]]
    i : int
    j : int
    result : int

    # on fixe les poids de chaque cases
    weight = [
        [5,3,5],
        [3,10,3],
        [5,3,5]
    ]
    result = 0

    for i in range(0,gameTicTacToe.sizeY):
        for j in range(0,gameTicTacToe.sizeX):
            if gameTicTacToe.plate[i][j] == currentPLayers.player2.playerNumber:
                result +=  weight[i][j]
            if gameTicTacToe.plate[i][j] == currentPLayers.player1.playerNumber:
                result -=  weight[i][j]
    return result

def customLevel(gameTicTacToe: GameTicTacToe, currentPlayers: CurrentPlayers,currentPlayer: Player, canBlock : list[bool]) -> tuple[int,int]:
    """
        Stratégie personnalisée pour le niveau de difficulté du jeu Tic Tac Toe.

        Args :
            - gameTicTacToe (GameTicTacToe) : L'instance du jeu Tic Tac Toe.
            - currentPlayers (CurrentPlayers) : Les joueurs actuels du jeu.
            - currentPlayer (Player) : Le joueur actuel (bot).
            - canBlock (list[bool]) : Un indicateur indiquant si le bot peut bloquer l'adversaire.

        Returns :
            - bestMove (tuple[int, int]) : Les coordonnées du meilleur coup choisi par le bot.
    """
    moves : list[tuple[int,int]]
    bestWeight : int
    weight : int
    bestMove : tuple[int,int]

    moves = remainingMoves(gameTicTacToe)
    if currentPlayer == currentPlayers.player1:
        currentPlayer = currentPlayers.player1
        #opponentPlayer = currentPlayers.player2
    else:
        currentPlayer = currentPlayers.player2
        #opponentPlayer = currentPlayers.player1

    # Vérifier s'il y a une possibilité de gagner au prochain coup
    for move in moves:
        gameTicTacToe.plate[move[0]][move[1]] = currentPlayer.playerNumber
        if checkWin(gameTicTacToe, currentPlayer):
            gameTicTacToe.plate[move[0]][move[1]] = 0  # Annuler le coup
            return move
        gameTicTacToe.plate[move[0]][move[1]] = 0  # Annuler le coup

    # Vérifier s'il y a une possibilité pour l'adversaire de gagner au prochain coup
    # bot trop fort au niveau 2 s'il peut bloquer
    """
    if canBlock[0]:
        for move in moves:
            gameTicTacToe.plate[move[0]][move[1]] = opponentPlayer.playerNumber
            if checkWin(gameTicTacToe, opponentPlayer):
                gameTicTacToe.plate[move[0]][move[1]] = 0  # Annuler le coup
                canBlock[0] = not canBlock[0]
                return move
            gameTicTacToe.plate[move[0]][move[1]] = 0  # Annuler le coup
    """
    # Si aucune possibilité de gagner ou de bloquer, jouer en utilisant les poids
    weights = [
        [5, 3, 5],
        [3, 10, 3],
        [5, 3, 5]
    ]

    bestMove = moves[0]
    bestWeight = 0

    for move in moves:
        # on destructure move et on met la case 0 dans i la case 1 dans j
        i, j = move
        if gameTicTacToe.plate[i][j] == 0:
            weight = weights[i][j]
            if weight > bestWeight:
                bestWeight = weight
                bestMove = move

    return bestMove

def remainingMoves(gameTicTacToe : GameTicTacToe) -> list[tuple[int,int]]:
    """
        Génère une liste des mouvements possibles restants sur le plateau du jeu Tic Tac Toe.

        Args:
            - gameTicTacToe (GameTicTacToe): L'instance du jeu Tic Tac Toe.

        Returns:
            - list[tuple[int, int]]: Liste des coordonnées des mouvements possibles restants.
    """

    i : int
    j : int
    tab : list[tuple[int,int]]

    tab = list()
    i = 0
    j = 0
    while i <  gameTicTacToe.sizeY:
        while j < gameTicTacToe.sizeX:
            # si la case contient 0 c'est qu'elle est libre
            if gameTicTacToe.plate[i][j] == 0 :
                tab.append((i,j))
            j+=1
        i+=1
        j = 0
    return tab

def botRandomPlay(gameTicTacToe : GameTicTacToe,currentPlayer :Player) -> None:
    """
        Effectue un mouvement aléatoire pour le bot dans le jeu Tic Tac Toe.

        Args:
            - gameTicTacToe (GameTicTacToe): L'instance du jeu Tic Tac Toe.
            - currentPlayer (Player): Le joueur actuel (bot).

    """
    el : int
    nbEls : int 
    moves: list[tuple[int,int]]
    move : tuple[int,int]

    moves  = remainingMoves(gameTicTacToe)
    nbEls = len(moves)
    if nbEls > 1 :
        el = randint(0, nbEls -1)
        move = moves[el] 
        gameTicTacToe.plate[move[0]][move[1]] = currentPlayer.playerNumber

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

def minimax(gameTicTacToe: GameTicTacToe, currentPlayers: CurrentPlayers,currentPayer : Player, depth: int, isMaxing: bool) -> int:
    """
        Implémente l'algorithme Minimax pour le jeu Tic Tac Toe.

        Args:
            - gameTicTacToe (GameTicTacToe): L'instance du jeu Tic Tac Toe.
            - currentPlayers (CurrentPlayers): Les joueurs actuels du jeu.
            - currentPlayer (Player): Le joueur actuel.
            - depth (int): La profondeur de recherche dans l'arbre de jeu.
            - isMaximizing (bool): Un indicateur indiquant si c'est le tour du joueur maximisant.

        Returns:
            - int: La valeur évaluée pour le meilleur mouvement possible.
    """
    move : tuple[int,int]
    eval : int
    min_eval : int
    max_eval : int
    
    if checkWin(gameTicTacToe, currentPlayers.player2):
        return 100
    elif checkWin(gameTicTacToe, currentPlayers.player1):
        return -100
    elif checkDraw(gameTicTacToe, currentPlayers.player2) or checkDraw(gameTicTacToe, currentPlayers.player1):
        return 0
    # si la profondeur atteint 0 on evalue la plateau de jeu avec la fonction heuristique
    elif depth == 0:
        return evaluateBoard(gameTicTacToe,currentPlayers, isMaxing)

    if isMaxing:
        max_eval = -10000
        for move in remainingMoves(gameTicTacToe):
            gameTicTacToe.plate[move[0]][move[1]] = currentPlayers.player2.playerNumber
            eval = minimax(gameTicTacToe, currentPlayers,currentPayer, depth - 1, not isMaxing)
            max_eval = max(max_eval, eval)
            gameTicTacToe.plate[move[0]][move[1]] = 0
    
        return max_eval
    else:
        min_eval = 10000
        for move in remainingMoves(gameTicTacToe):
            gameTicTacToe.plate[move[0]][move[1]] = currentPlayers.player1.playerNumber
            eval = minimax(gameTicTacToe, currentPlayers,currentPayer, depth - 1, not isMaxing)
            min_eval = min(min_eval, eval)
            gameTicTacToe.plate[move[0]][move[1]] = 0
            
        return min_eval

def chooseBestMove(gameTicTacToe: GameTicTacToe, currentPlayers: CurrentPlayers, currentPlayer: Player) -> None:
    """
        Choisi le meilleur mouvement pour le joueur actuel dans le jeu Tic Tac Toe en prenant en compte le niveau attribué.

        Args:
            - gameTicTacToe (GameTicTacToe): L'instance du jeu Tic Tac Toe.
            - currentPlayers (CurrentPlayers): Les joueurs actuels du jeu.
            - currentPlayer (Player): Le joueur actuel.

    """
    moves : list[tuple[int,int]]
    eval: float
    first_move : bool
    depth : int
    canBlock : list[bool]

    first_move = False
    canBlock = [True]
    moves = list()

    moves = remainingMoves(gameTicTacToe)
    bestEval = -10000 if currentPlayer == currentPlayers.player2 else 10000
    if (1,1) in moves and len(moves) == 9:
        bestMove = (1,1)
        first_move = True
    else:
        bestMove =  moves[0]

    if currentPlayer.lvl == 4:
        depth = 1 #profondeur de 1 pour que le niveau du bot soit moins bon
    else:
        depth = 9 #profondeur max
    random = randint(1,10)
    if currentPlayer.lvl == 2:
        bestMove = customLevel(gameTicTacToe,currentPlayers,currentPlayer,canBlock)
        gameTicTacToe.plate[bestMove[0]][bestMove[1]] = currentPlayer.playerNumber

    elif (currentPlayer.lvl == 3 and random > 7) or (currentPlayer.lvl == 1):
        print("randomPlay")
        botRandomPlay(gameTicTacToe,currentPlayer)
    elif not first_move:
        for move in remainingMoves(gameTicTacToe):
            gameTicTacToe.plate[move[0]][move[1]] = currentPlayer.playerNumber
            
            eval = minimax(gameTicTacToe, currentPlayers,currentPlayer, depth, currentPlayer == currentPlayers.player1)
            gameTicTacToe.plate[move[0]][move[1]] = 0

            if (currentPlayer == currentPlayers.player2 and eval > bestEval) or (currentPlayer == currentPlayers.player1 and eval < bestEval):
                bestEval = eval
                bestMove = move

        gameTicTacToe.plate[bestMove[0]][bestMove[1]] = currentPlayer.playerNumber
    else:
        # dans certains cas on veut que le bot pour son premier coup joue au milieu s'il commence
        gameTicTacToe.plate[bestMove[0]][bestMove[1]] = currentPlayer.playerNumber
        # on met first_move à False pour qu'on ne revienne pas dans cette partie
        first_move = False

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
    configureBotsLevel(currentPlayers)
    print("vous allez joueur sur cette grille")

    displayGrid(gameTicTacToe,currentPlayers)
    currentPlayer = currentPlayers.player1
    while not finished:
        print(setColorGreen("("+ currentPlayer.name + ")") + " à toi de jouer")
        # ajout de temps de réponse pour l'experience utilisateur
        time.sleep(1)
        if currentPlayer.isBot:
            chooseBestMove(gameTicTacToe,currentPlayers,currentPlayer)
            displayGrid(gameTicTacToe, currentPlayers)
            #si il y a une victoire ou une égalité on arrete le jeu 
            if checkWin(gameTicTacToe,currentPlayer) or checkDraw(gameTicTacToe,currentPlayer):
                finished = True
            else:
                currentPlayer = getOtherPlayer(currentPlayers,currentPlayer)
        else:
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
                #si il y a une victoire ou une égalité on arrete le jeu 
                if checkWin(gameTicTacToe,currentPlayer) or checkDraw(gameTicTacToe,currentPlayer):
                    finished = True
                else:
                    currentPlayer = getOtherPlayer(currentPlayers,currentPlayer)
    winningInformationsInit(winningInformations, gameTicTacToe.colName,gameTicTacToe.pointDraw,gameTicTacToe.pointWin,gameTicTacToe.pointLoose,checkDraw(gameTicTacToe,currentPlayer))
    pointsDistribution(winningInformations,currentPlayers,currentPlayer,conn)    
