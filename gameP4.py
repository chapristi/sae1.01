from colors import set_color_red,set_color_yellow
class GameP4:
    colName : str
    pointWin : int
    pointLoose : int
    pointDraw: int
    player1Pawn : str
    player2Pawn : str
    size_x : int
    size_y : int
    plate : list[list[int]]


def gameP4Init(gameP4 : GameP4):
    gameP4.colName = "scoreP4"
    gameP4.player1Pawn = set_color_yellow("⬤")
    gameP4.player2Pawn = set_color_red("⬤")
    gameP4.pointWin = 5
    gameP4.pointDraw = 2
    gameP4.pointLoose = 1
    gameP4.size_x = 7
    gameP4.size_y = 6
    gameP4.plate = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
        ]
