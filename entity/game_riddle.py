from utils.input_checker import isDigit
from entity.player import CurrentPlayers
from utils.colors import set_color_green,set_color_yellow
import getpass

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
        le nombre à deviner (entre 0 et 200) et le nombre d'essaie qu'il donne au joueur qui devine.
    
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
    numberToGuess = getpass.getpass("(" + set_color_green(currentPlayers.player1.name)+ ")"+ " Entrez le nombre à deviner entre 0 et 200")
    while not isDigit(numberToGuess) or int(numberToGuess) <  0 or int(numberToGuess) > 200:
        numberToGuess = getpass.getpass("(" + set_color_green(currentPlayers.player1.name)+ ")"+ set_color_yellow("Entrez le nombre à deviner entre 0 et 200"))
    maxAttempts = input("(" + set_color_green(currentPlayers.player1.name)+ ")"+ " ⚠️Entrez le nombre de tentative qu'aura le joueur >1 ")
    while not isDigit(maxAttempts) or int(maxAttempts) < 1:
        maxAttempts = input("(" + set_color_green(currentPlayers.player1.name)+ ")"+ set_color_yellow(" ⚠️Entrez le nombre de tentative qu'aura le joueur >1 "))
        
    gameRiddle.maxAttempts = int(maxAttempts)
    gameRiddle.numberToGuess = int(numberToGuess)