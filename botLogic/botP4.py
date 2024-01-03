from entity.gameP4 import *
from entity.player import *
from random import randint
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
    # calcul du poids des cases pour les deux joueurs
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