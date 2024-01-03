from entity.player import *
from entity.gameTicTacToe import *
from random import randint



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
    if nbEls > 0 :
        el = randint(0, nbEls -1)
        move = moves[el] 
        gameTicTacToe.plate[move[0]][move[1]] = currentPlayer.playerNumber


