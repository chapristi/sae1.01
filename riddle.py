from entity.gameRiddle import *
from entity.player import *
from helpers.inputChecker import isDigit
from sqlite3 import Connection
from helpers.colors import *
from helpers.pointRepartition import pointsDistribution
from entity.winningInformations import *
from helpers.startingMenu import displayStartingMenu

def calcPoints(attempts: int, max_attempts: int, point_win:int) -> int:
    """
    Calcule les points en fonction du nombre d'essais et du nombre maximal d'essais autorisé.

    Args:
        attempts (int): Le nombre d'essais effectués.
        max_attempts (int): Le nombre maximal d'essais autorisé.
        point_win (int): Le nombre de points à attribuer en cas de victoire.

    Returns:
        int: Le nombre de points attribués.
    """
    if attempts <= 0 or max_attempts <= 0:
        return 0  # Éviter la division par zéro

    points = 1 - (max_attempts / attempts)
    points = min(1, points)  # Limiter le score à 1 au maximum
    points *= point_win

    return max(1, int(points))  # Assurer un minimum de 1 point attribué

def guessNumber(gameRiddle : GameRiddle, information : str, choice : int) -> bool:
    """
    Vérifie si le joueur 1 ment sur le résultat de la devinette dans le jeu de devinette (Riddle).

    Args:
        gameRiddle (GameRiddle): L'objet GameRiddle de la partie en cours.
        information (str): L'information fournie par le joueur ("plus", "moins", ou "egal").
        choice (int): Le choix du joueur quant au nombre à deviner.

    Returns:
        bool: True si le joueur ment sur le résultat, sinon False.
    """
    isLiar : bool

    isLiar = True
    if choice > gameRiddle.numberToGuess and information == "trop grand":
        isLiar = False
    elif choice < gameRiddle.numberToGuess and information == "trop petit":
        isLiar = False
    elif choice == gameRiddle.numberToGuess and information == "c'est gagné":
        isLiar = False
    return isLiar


def game(currentPlayers: CurrentPlayers, conn: Connection)->None:
    """
        Cette fonction gère le déroulement du jeu de devinette, où un joueur doit deviner un nombre.

        Args:
            currentPlayers (CurrentPlayers): L'objet contenant les joueurs actuels.
            conn (Connection): L'objet de connexion.

        Returns:
            None
    """
    gameRiddle : GameRiddle
    information : str
    winningInformations : WinningInformations
    winner: Player
    choice : str

    gameRiddle = GameRiddle()
    winningInformations = WinningInformations()
    displayStartingMenu("Jeu des devinettes", [
        "REGLES DU JEU :" ,
        "1. Le joueur 1 choisi le nombre que le joueur 2 va devoir trouvé se situant entre (0 et 200) ainsi que le nombre de tentative max que le joueur deux a pour trouver (> 1) le nombre ",
        "2. Le joueur deux donne alors un nombre qui pense etre le bon ",
        "3. Le joueur 2 indique au joueur un si le nombre donné est (trop petit trop grand ou c'est gagné)",
        "4. Le jeu s'arrete quand le joeur 2 à trouvé le bon nombre dans le nombre de coups imparti ou quand son nombre de tentative a depasser le nombre de tentatives maximale"
    ])
    winner = currentPlayers.player1
    gameRiddleInit(gameRiddle,currentPlayers)
    while not gameRiddle.isOver:
        gameRiddle.attempts += 1
        choice = input("(" + setColorGreen(currentPlayers.player2.name)+ ")"+" Essayez de trouver le nombre")
        while not isDigit(choice):
            choice = input("(" + setColorGreen(currentPlayers.player2.name)+ ")"+" Essayez de trouver le nombre")
        information = input("(" + setColorGreen(currentPlayers.player1.name)+ ")"+ " Entrez (trop petit), (trop grand) ou (c'est gagné) en fonction du nombre entree")
        while guessNumber(gameRiddle,information,int(choice)):
            information = input("(" + setColorGreen(currentPlayers.player1.name)+ ")"+" ne mentez pas! Entrez (trop petit), (trop grand) ou (c'est gagné) en fonction du nombre entree")
        if int(choice) == gameRiddle.numberToGuess:
            winner = currentPlayers.player2
            gameRiddle.isOver = True
        elif gameRiddle.attempts >= gameRiddle.maxAttempts:
            winner = currentPlayers.player1
            gameRiddle.isOver = True
    winningInformationsInit(winningInformations, gameRiddle.colName,0,calcPoints(gameRiddle.attempts,gameRiddle.maxAttempts,gameRiddle.pointWin),gameRiddle.pointLoose,False)
    pointsDistribution(winningInformations,currentPlayers,winner,conn)

   