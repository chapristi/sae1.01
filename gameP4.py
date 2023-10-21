from colors import set_color_red,set_color_yellow
class GameP4:
    pointWin : int
    pointLoose : int
    pointDraw: int
    player1Pawn : str
    player2Pawn : str
    player1Number : int
    player2Number : int
    player1Shifts : int 
    player2Shifts : int
    size_x : int
    size_y : int
    plate : list[list[int]]
    isOver : bool


def gameP4Init(gameP4 : GameP4):
    #a voir si les shift sont interessants
    # pour savoir si le jeu est fini on check si il restev des cases à 0
    gameP4.isOver = False
    gameP4.player1Pawn = set_color_yellow("⬤")
    gameP4.player2Pawn = set_color_red("⬤")
    gameP4.player1Number = 2
    gameP4.player2Number = 3
    gameP4.player1Shifts = 21
    gameP4.player2Shifts = 21
    gameP4.pointWin = 2
    gameP4.pointDraw = 1
    gameP4.pointLoose = 10
    gameP4.size_x = 7
    gameP4.size_y = 6
    gameP4.plate = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,3,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,2]
        ]
