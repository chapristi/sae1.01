from input_checker import isDigit
class GameRiddle:
    pointWin : int
    pointLoose : int
    numberToGuess : int
    maxAttempts : int
    attempts : int
    isOver : bool

def gameRiddleInit(gameRiddle : GameRiddle)->None:
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

    gameRiddle.pointLoose = 1
    gameRiddle.pointLoose = 100
    gameRiddle.isOver = False
    gameRiddle.attempts = 0
    numberToGuess = input("entrez le nombre à deviner")
    while not isDigit(numberToGuess) and int(numberToGuess) <  0:
        numberToGuess = input("entrez le nombre à deviner")
    maxAttempts = input("entrez la fin de l'interval > 1")
    while not isDigit(maxAttempts) and int(maxAttempts) < 1:
        numberToGuess = input("entrez la fin de l'interval > 1")
        
    gameRiddle.maxAttempts = int(maxAttempts)
    gameRiddle.numberToGuess = int(numberToGuess)