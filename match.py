#from player import CurrentPlayers
from entity.gameMatch import GameMatch, gameMatchInit
from helpers.colors import setColorGreen,setColorRed,setColorYellow
from helpers.inputChecker import isDigit
from sqlite3 import Connection
from entity.player import *
from dataServices.sqlCommands import addPoint
from helpers.helperPlayer import getOtherPlayer

def displayStartingMenu() -> None:
    """
        Affiche le menu de démarrage du jeu des Allumettes.

        Cette fonction affiche le menu de démarrage du jeu des Allumettes, y compris les règles du jeu, un message de bienvenue et un message de chargement.

        Args:
            None

        Returns:
            None
    """
    print(setColorGreen("RÉGLES DU JEU \n 1. On distribue 20 allumettes par joueur \n 2. Chacun son tour pose un bâtonnet sur le goulot d'une bouteille vide. \n 3. Si un joueur maladroit fait tomber les allumettes en plaçant la sienne, il les récupère toutes ! \n 4. Le premier qui n'a plus d'allumettes a gagné ! \n 5. Chaque joueur a seulement le droit de prendre un maximum de 3 allumette "))
    print(setColorGreen("Bienvenue sur le jeu des Allumettes etes vous pret a jouer?"))

def displayWin(winner : Player, currentPLayers: CurrentPlayers,gameMatch : GameMatch) -> None:
    """
        Affiche le résultat de la partie.

        Cette fonction affiche le résultat de la partie, en indiquant le joueur gagnant et le joueur perdant, ainsi que le nombre de points gagnés par le gagnant.

        Args:
            winner (Player): L'instance de la classe Player correspondant au joueur gagnant.
            currentPlayers (CurrentPlayers): L'instance de la classe CurrentPlayers contenant les deux joueurs.
            gameMatch (GameMatch): L'instance de la classe GameMatch représentant le match en cours.

        Returns:
            None
    """
    looser : Player

    looser = getOtherPlayer(currentPLayers,winner)
    print(setColorGreen("Bravo c'est ("+  winner.name + ") qui l'emporte et gagne +"+ str(gameMatch.pointWin)+" points"))
    print(setColorYellow("Dommage c'est (" + looser.name + ") qui a perdu mais remporte +"+ str(gameMatch.pointLoose)+" points"))

def pointsRepartition(gameMatch : GameMatch,conn :Connection,currentPlayers:CurrentPlayers,winner:Player)->None:
    """
        Répartit les points pour un match entre deux joueurs.

        Cette fonction répartit les points pour un match entre deux joueurs, enregistrant les points du gagnant et du perdant dans la base de données via la connexion `conn`.

        Args:
            gameMatch (GameMatch): L'instance de la classe GameMatch représentant le match en cours.
            conn (Connection): L'objet de connexion à la base de données pour enregistrer les points.
            currentPlayers (CurrentPlayers): L'instance de la classe CurrentPlayers contenant les deux joueurs.
            winner (Player): L'instance de la classe Player correspondant au joueur gagnant.

        Returns:
            None
    """
    looser : Player

    looser = getOtherPlayer(currentPlayers,winner)
    addPoint(winner.id,gameMatch.pointWin,conn,gameMatch.colName)
    addPoint(looser.id,gameMatch.pointLoose,conn,gameMatch.colName)
  
def drawMatches(nb : int) -> None:
    """
        Dessine des allumettes colorées.

        Cette fonction dessine des allumettes colorées en fonction du nombre spécifié (`nb`) en utilisant des caractères de couleur.

        Args:
            nb (int): Le nombre d'allumettes à dessiner.

        Returns:
            None
    """
    matches : list[str]
    i : int
    j : int

    i = 0
    j = 0
    matches = [
         setColorRed("█"),
         setColorYellow ("█"),
         setColorYellow ("█"),
         setColorYellow ("█"),
         setColorYellow ("█"),
    ]
    for i in range(0,5):
        print()
        while j < nb:
            print(matches[i] + " ",end="")
            j+=1
        j = 0
    print()


    
def game(currentPlayers : CurrentPlayers, conn : Connection) -> None:
    """
        Gère le déroulement du jeu des allumettes entre deux joueurs.

        Cette fonction gère le déroulement du jeu des allumettes entre deux joueurs. Elle initialise le jeu, affiche le menu de démarrage, permet aux joueurs de retirer des allumettes tour à tour, vérifie si la partie est terminée, affiche le résultat et répartit les points en conséquence.

        Args:
            currentPlayers (CurrentPlayers): L'instance de la classe CurrentPlayers contenant les deux joueurs.
            conn (Connection): L'objet de connexion à la base de données pour enregistrer les points.
        Returns:
            None
    """
    
    gameMatch : GameMatch
    currPlayer : Player
    choice  : str

    currPlayer = currentPlayers.player1
    gameMatch = GameMatch()
    gameMatchInit(gameMatch)
    displayStartingMenu()

    while gameMatch.numberOfMatches > 0:
        drawMatches(gameMatch.numberOfMatches)
        print(setColorGreen(currPlayer.name), "à vous de jouer")
        choice = input("choisissez entre " + setColorYellow("1,2 ou 3") +" allumettes à retirer ")
        
        while not isDigit(choice) or int(choice) < 1 or int(choice) > 3:
            choice = input(
                setColorYellow("⚠️ choisissez entre 1,2 ou 3 allumettes à retirer")
            )
        gameMatch.numberOfMatches -= int(choice)
        currPlayer = getOtherPlayer(currentPlayers,currPlayer)

    displayWin(currPlayer,currentPlayers,gameMatch)
    pointsRepartition(gameMatch,conn,currentPlayers,currPlayer)
              



