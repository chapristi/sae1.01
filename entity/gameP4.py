from utils.colors import set_color_red,set_color_yellow
class GameP4:
    colName : str
    pointWin : int
    pointLoose : int
    pointDraw: int
    player1Pawn : str
    player2Pawn : str
    sizeX : int
    sizeY : int
    plate : list[list[int]]


def gameP4Init(gameP4 : GameP4):
    """
        Initialise un objet GameP4 avec les paramètres spécifiques.

        Cette fonction initialise un objet GameP4 avec des paramètres spécifiques pour le jeu Puissance 4, tels que le nom de la colonne pour enregistrer les scores, les symboles des joueurs, les points attribués en cas de victoire, égalité ou défaite, ainsi que la taille de la grille et l'état initial de la grille.

        Args:
            gameP4 (GameP4): L'objet GameP4 à initialiser.

        Returns:
            None

    """

    gameP4.colName = "scoreP4"
    gameP4.player1Pawn = set_color_yellow("⬤")
    gameP4.player2Pawn = set_color_red("⬤")
    gameP4.pointWin = 5
    gameP4.pointDraw = 2
    gameP4.pointLoose = 1
    gameP4.sizeX = 7
    gameP4.sizeY = 6
    gameP4.plate = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
        ]
