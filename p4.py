from gameP4 import GameP4,gameP4Init
from player import CurrentPlayers
from colors import set_color_blue
def checkWin(gameP4 : GameP4):
    pass
def checkDraw(gameP4 : GameP4)->bool:
    i : int
    j : int
    isDraw: bool

    isDraw = True
    if checkWin(gameP4):
        return not isDraw
    for i in range(0,gameP4.size_y):
        for j in range(0, gameP4.size_x):
            if gameP4.plate[i][j] == 0:
                isDraw  = False
    return isDraw

def play(gameP4 : GameP4, column :int, number : int)->bool:
    i : int
    canPlay : bool

    canPlay = False
    i = 0
    for i in range(0,gameP4.size_x):
        if gameP4.plate[i][column]  == 0:
            gameP4.plate[i][column] = number
            canPlay = True
    return canPlay

     
    
def displayGrid(gameP4 : GameP4)->None:
    i : int
    j : int

    i = 0 
    j = 0
    for i in range(0,gameP4.size_y):
        print(set_color_blue("+") + set_color_blue("----+")*gameP4.size_x)
        print(set_color_blue("|"),end="")
        for j in range(0,gameP4.size_x):
            if gameP4.plate[i][j] == gameP4.player1Number:
                print(f" {gameP4.player1Pawn}  "+set_color_blue("|"),end="")
            elif gameP4.plate[i][j] == gameP4.player2Number:
                print(f" {gameP4.player2Pawn}  "+set_color_blue("|"),end="")
            else:
                print(f"    "+set_color_blue("|"),end="")
        print()
    print(set_color_blue("+") + set_color_blue("----+")*gameP4.size_x)


def game(currentPlayer : CurrentPlayers):
    gameP4 : GameP4
    finished : bool

    finished = False
    gameP4 = GameP4()
    gameP4Init(gameP4)
    displayGrid(gameP4)
    while not finished:




game()
