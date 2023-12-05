from entity.gameRiddle import *
from entity.player import *
from helpers.inputChecker import isDigit
from sqlite3 import Connection
from helpers.colors import *
from helpers.pointRepartition import pointsDistribution
from entity.winningInformations import *
from helpers.startingMenu import displayStartingMenu

def calcPoints(attempts: int, maxAttempts: int, pointWin: int) -> int:
    """
    Calcule les points en fonction du nombre d'essais et du nombre maximal d'essais autorisé.

    Args:
        attempts (int): Le nombre d'essais effectués.
        maxAttempts (int): Le nombre maximal d'essais autorisé.
        pointWin (int): Le nombre de points à attribuer en cas de victoire.

    Returns:
        int: Le nombre de points attribués.
    """
    if attempts <= 0 or maxAttempts <= 0:
        return 0  # Éviter la division par zéro

    if attempts == 1:
        return pointWin  # Si l'utilisateur trouve en 1 essai, attribuer le maximum de points

    points = 1 - (attempts - 1) / maxAttempts
    points = max(0, points)  # Limiter le score à 0 au minimum
    points *= pointWin

    return min(pointWin, int(points))  # Assurer un maximum de 15 points attribués


def guessNumber(gameRiddle : GameRiddle, information : int , choice : int) -> bool:
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
    if choice > gameRiddle.numberToGuess and information == 1:
        isLiar = False
    elif choice < gameRiddle.numberToGuess and information == 2:
        isLiar = False
    elif choice == gameRiddle.numberToGuess and information == 3:
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
    #initialisation du jeu
    gameRiddleInit(gameRiddle,currentPlayers)
    while not gameRiddle.isOver:
        gameRiddle.attempts += 1
        choice = input("(" + setColorGreen(currentPlayers.player2.name)+ ")"+" Essayez de trouver le nombre ")
        while not isDigit(choice):
            choice = input("(" + setColorGreen(currentPlayers.player2.name)+ ")"+" Essayez de trouver le nombre")
        information = input("(" + setColorGreen(currentPlayers.player1.name)+ ")"+ " Entrez (trop petit => 1), (trop grand => 2) ou (c'est gagné => 3) en fonction du nombre entree ")
        #verification si le joueur 1 ment sur le resultat
        while not isDigit(information) and guessNumber (gameRiddle,int(information),int(choice)):
            information = input("(" + setColorGreen(currentPlayers.player1.name)+ ")"+" ne mentez pas! Entrez (trop petit => 1), (trop grand => 2) ou (c'est gagné => 3) en fonction du nombre entree ")
        if int(choice) == gameRiddle.numberToGuess:
            winner = currentPlayers.player2
            gameRiddle.isOver = True
        elif gameRiddle.attempts >= gameRiddle.maxAttempts:
            winner = currentPlayers.player1
            gameRiddle.isOver = True
    winningInformationsInit(winningInformations, gameRiddle.colName,0,calcPoints(gameRiddle.attempts,gameRiddle.maxAttempts,gameRiddle.pointWin),gameRiddle.pointLoose,False)
    pointsDistribution(winningInformations,currentPlayers,winner,conn)

   