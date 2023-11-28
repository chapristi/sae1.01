# from player import CurrentPlayers
from entity.gameMatch import GameMatch, gameMatchInit
from helpers.colors import setColorGreen, setColorRed, setColorYellow
from helpers.inputChecker import isDigit
from sqlite3 import Connection
from entity.player import *
from entity.winningInformations import *
from helpers.helperPlayer import getOtherPlayer
from helpers.startingMenu import displayStartingMenu
from helpers.pointRepartition import pointsDistribution

def drawMatches(nb: int) -> None:
    """
        Dessine des allumettes colorées.

        Cette fonction dessine des allumettes colorées en fonction du nombre spécifié (`nb`) en utilisant des caractères de couleur.

        Args:
            nb (int): Le nombre d'allumettes à dessiner.

        Returns:
            None
    """
    matches: list[str]
    i: int
    j: int

    i = 0
    j = 0
    matches = [
        setColorRed("█"),
        setColorYellow("█"),
        setColorYellow("█"),
        setColorYellow("█"),
        setColorYellow("█"),
    ]
    for i in range(0, 5):
        print()
        while j < nb:
            print(matches[i] + " ", end="")
            j += 1
        j = 0
    print()


def game(currentPlayers: CurrentPlayers, conn: Connection) -> None:
    """
        Gère le déroulement du jeu des allumettes entre deux joueurs.

        Cette fonction gère le déroulement du jeu des allumettes entre deux joueurs. Elle initialise le jeu, affiche le menu de démarrage, permet aux joueurs de retirer des allumettes tour à tour, vérifie si la partie est terminée, affiche le résultat et répartit les points en conséquence.

        Args:
            currentPlayers (CurrentPlayers): L'instance de la classe CurrentPlayers contenant les deux joueurs.
            conn (Connection): L'objet de connexion à la base de données pour enregistrer les points.
        Returns:
            None
    """

    gameMatch: GameMatch
    currPlayer: Player
    choice: str
    winningInformations : WinningInformations

    currPlayer = currentPlayers.player1
    gameMatch = GameMatch()
    winningInformations = WinningInformations()
    gameMatchInit(gameMatch)
    displayStartingMenu("Jeu des Allumettes",[
        "RÉGLES DU JEU : ",
        "1. On distribue 20 allumettes par joueur ",
        "2. Chacun son tour pose un bâtonnet sur le goulot d'une bouteille vide. ",
        "3. Si un joueur maladroit fait tomber les allumettes en plaçant la sienne, il les récupère toutes ! ",
        "4. Le premier qui n'a plus d'allumettes a gagné ! ",
        "5. Chaque joueur a seulement le droit de prendre un maximum de 3 allumette"
    ])

    while gameMatch.numberOfMatches > 0:
        drawMatches(gameMatch.numberOfMatches)
        print(setColorGreen(currPlayer.name), "à vous de jouer")
        choice = input("choisissez entre " +
                       setColorYellow("1,2 ou 3") + " allumettes à retirer ")

        while not isDigit(choice) or int(choice) < 1 or int(choice) > 3:
            choice = input(
                setColorYellow(
                    "⚠️ choisissez entre 1,2 ou 3 allumettes à retirer")
            )
        gameMatch.numberOfMatches -= int(choice)
        currPlayer = getOtherPlayer(currentPlayers, currPlayer)
    winningInformationsInit(winningInformations, gameMatch.colName,0,gameMatch.pointWin,gameMatch.pointLoose,False)
    pointsDistribution(winningInformations,currentPlayers,currPlayer,conn)
