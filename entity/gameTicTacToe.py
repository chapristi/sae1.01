class GameTicTacToe:
    colName : str
    pointWin : int
    pointLoose : int
    pointDraw: int
    player1Pawn : str
    player2Pawn : str
    size_x : int
    size_y : int
    plate : list[list[int]]


def gameTicTacToeInit(gameTicTacToe : GameTicTacToe):
    """
        Initialise un objet GameTicTacToe avec les paramètres spécifiques.

        Cette fonction initialise un objet GameTicTacToe avec des paramètres spécifiques pour le jeu Tic Tac Toe, tels que le nom de la colonne pour enregistrer les scores, les symboles des joueurs, les points attribués en cas de victoire, égalité ou défaite, ainsi que la taille de la grille et l'état initial de la grille.

        Args:
            gameTicTacToe (GameTicTacToe): L'objet GameTicTacToe à initialiser.

        Returns:
            None

    """
    gameTicTacToe.colName = "scoreTtt"
    gameTicTacToe.player1Pawn = "X"
    gameTicTacToe.player2Pawn = "O"
    gameTicTacToe.pointWin = 5
    gameTicTacToe.pointDraw = 2
    gameTicTacToe.pointLoose = 1
    gameTicTacToe.size_x = 3
    gameTicTacToe.size_y = 3
    gameTicTacToe.plate = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
        ]
