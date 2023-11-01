from input_checker import isDigit
from player import CurrentPlayers
from colors import set_color_green
class GameRiddle:
    colName : str
    pointWin : int
    pointLoose : int
    numberToGuess : int
    maxAttempts : int
    attempts : int
    isOver : bool

def gameRiddleInit(gameRiddle : GameRiddle, currentPlayers : CurrentPlayers)->None:
    """
        Initialise les attributs de l'objet GameRiddle en demandant à l'utilisateur de saisir
        le nombre à deviner et l'intervalle.
    
        Args:
            gameRiddle (GameRiddle): variable de type GameRiddle.
        Returns:
            Rien
    """
    numberToGuess : str
    maxAttempts : str

    gameRiddle.pointLoose = 2
    gameRiddle.pointWin = 15
    gameRiddle.colName = "scoreRiddle"
    gameRiddle.isOver = False
    gameRiddle.attempts = 0
    numberToGuess = input("(" + set_color_green(currentPlayers.player1.name)+ ")"+ " entrez le nombre à deviner")
    while not isDigit(numberToGuess) and int(numberToGuess) <  0:
        numberToGuess = input("(" + set_color_green(currentPlayers.player1.name)+ ")"+ "entrez le nombre à deviner")
    maxAttempts = input("(" + set_color_green(currentPlayers.player1.name)+ ")"+ " entrez le nombre de tentative >1 ")
    while not isDigit(maxAttempts) and int(maxAttempts) < 1:
        numberToGuess = input("(" + set_color_green(currentPlayers.player1.name)+ ")"+ " entrez le nombre de tentative >1 ")
        
    gameRiddle.maxAttempts = int(maxAttempts)
    gameRiddle.numberToGuess = int(numberToGuess)