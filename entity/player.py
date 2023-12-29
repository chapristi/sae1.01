from helpers.colors import *
from helpers.inputChecker import isDigit

class Player:
    id : int
    name : str
    playerNumber : int
    isBot : bool
    lvl : int
    

def playerInit(player : Player,id : int,name : str,isBot : bool,level: int)->None:
    """
        Initialise un objet joueur avec les informations fournies.

        Cette fonction initialise un objet joueur avec un identifiant, un nom et les scores pour différents jeux.

        Args:
            player (Player): L'objet de joueur à initialiser.
            id (int): L'identifiant du joueur.
            name (str): Le nom du joueur.
         

        Returns:
            None
    """
    player.id = id
    player.name = name
    player.lvl = level
    player.isBot = isBot





class CurrentPlayers:
    player1 : Player
    player2 : Player


def currentPlayersInit(curentPlayers : CurrentPlayers, player1 : Player, player2 : Player)->None:
    """
        Initialise l'objet CurrentPlayers avec les deux joueurs.

        Cette fonction initialise l'objet CurrentPlayers avec les deux joueurs fournis et attribue des numéros de joueur uniques à chacun d'eux.

        Args:
            currentPlayers (CurrentPlayers): L'objet CurrentPlayers à initialiser.
            player1 (Player): Le premier joueur.
            player2 (Player): Le deuxième joueur.

        Returns:
            None
    """
    curentPlayers.player1 = player1
    curentPlayers.player2 = player2
    curentPlayers.player1.playerNumber = 2
    curentPlayers.player2.playerNumber = 3

def changeBotLevel(player : Player):
    if player.isBot:
        choice = input(f"Configurer le niveau de {player.name} ? (O/n) ").lower()
        if choice == "o" or choice == "":
            level = input("Entrez le niveau (1 à 5): ")
            while not isDigit(level) or not (1 <= int(level) <= 5):
                print("Niveau invalide. Veuillez entrer un nombre entre 1 et 5.")
                level = input("Entrez le niveau (1 à 5): ")
            player.lvl = int(level)

def configureBotsLevel(currentPlayers : CurrentPlayers):
    for player in [currentPlayers.player1, currentPlayers.player2]:
        changeBotLevel(player)
   