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
