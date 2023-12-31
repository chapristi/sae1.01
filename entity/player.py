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

        Cette fonction initialise un objet joueur avec un identifiant, un nom, et un niveau.

        Args:
            - player (Player): L'objet joueur à initialiser.
            - id (int): L'identifiant du joueur.
            - name (str): Le nom du joueur.
            - isBot (bool): Indique si le joueur est un bot.
            - level (int): Le niveau du joueur.

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
    """
        Permet à l'utilisateur de configurer le niveau d'un joueur bot.

        Cette fonction vérifie si le joueur est un bot et invite l'utilisateur à configurer son niveau.

        Args:
            - player (Player): L'objet joueur dont le niveau doit être configuré.
    """
    level : str

    if player.isBot:
        choice = input(f"Configurer le niveau de {player.name} ? (O/n) ").lower()
        if choice == "o" or choice == "":
            level = input("Entrez le niveau (1 à 5): ")
            while not isDigit(level) or not (1 <= int(level) <= 5):
                print("Niveau invalide. Veuillez entrer un nombre entre 1 et 5.")
                level = input("Entrez le niveau (1 à 5): ")
            player.lvl = int(level)

def configureBotsLevel(currentPlayers : CurrentPlayers):
    """
        Configure les niveaux des joueurs bots dans l'objet CurrentPlayers.

        Cette fonction itère sur les joueurs dans l'objet CurrentPlayers et configure leurs niveaux s'ils sont des bots.

        Args:
            - currentPlayers (CurrentPlayers): L'objet CurrentPlayers contenant les joueurs du jeu.
    """
    player : Player

    for player in [currentPlayers.player1, currentPlayers.player2]:
        changeBotLevel(player)
   