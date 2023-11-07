from entity.gameRiddle import *
from entity.player import *
from utils.inputChecker import isDigit
from sqlite3 import Connection
from utils.colors import *
from dataServices.sqlCommands import addPoint
from helperPlayer import getOtherPlayer

def display_result(gameRiddle : GameRiddle, looser: Player, winner: Player):
    """
        Affiche les résultats d'une partie.

        Cette fonction affiche le résultat d'une partie en donnant des informations sur le gagnant et le perdant, ainsi que le nombre de points gagnés et perdus.

        Args:
            gameRiddle (GameRiddle): L'instance de la classe GameRiddle correspondant à la partie.
            looser (Player): L'instance de la classe Player correspondant au perdant.
            winner (Player): L'instance de la classe Player correspondant au gagnant.

        Returns:
            None
    """
     
    print(set_color_green("\nBravo (" + winner.name + ") vous avez gagné , vous recevez " + str(gameRiddle.pointWin) + " points"))
    print(set_color_yellow("Merci de votre participation (" + looser.name + "), vous recevez " + str(gameRiddle.pointLoose) + " points"))


def guess_number(gameRiddle : GameRiddle, information : str, choice : int) -> bool:
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

def pointsDistribution(gameRiddle : GameRiddle, winner: Player, looser : Player ,conn : Connection):
    """
    Distribue les points aux joueurs gagnants et perdants dans le jeu de devinette (Riddle).

    La fonction utilise la fonction `addPoint` pour ajouter des points aux joueurs gagnants et perdants en fonction des
    points attribués dans l'objet gameRiddle. Les points sont ajoutés à la base de données avec l'ID du joueur et le nom
    de la colonne spécifié dans gameRiddle.

    Args:
        gameRiddle (GameRiddle): L'objet GameRiddle de la partie en cours.
        winner (Player): Le joueur gagnant.
        looser (Player): Le joueur perdant.
        conn (Connection): L'objet de connexion à la base de données.

    Returns:
        None

    """
    
    addPoint(winner.id,gameRiddle.pointWin,conn,gameRiddle.colName)
    addPoint(looser.id,gameRiddle.pointLoose,conn,gameRiddle.colName)

    
def game(currentPlayers: CurrentPlayers, conn : Connection):
    """
        Cette fonction gère le déroulement du jeu de devinette, où un joueur doit deviner un nombre.

        Args:
            currentPlayers (CurrentPlayers): L'objet contenant les joueurs actuels.
            conn (Connection): L'objet de connexion.

        Returns:
            None
    """
    gameRiddle : GameRiddle
    gameRiddle = GameRiddle()
    information : str 
    winner: Player
    looser : Player
    choice : str
    winner = currentPlayers.player1
    gameRiddleInit(gameRiddle,currentPlayers)
    while not gameRiddle.isOver:
        gameRiddle.attempts += 1
        choice = input("(" + set_color_green(currentPlayers.player2.name)+ ")"+" Essayez de trouver le nombre")
        while not isDigit(choice):
            choice = input("(" + set_color_green(currentPlayers.player2.name)+ ")"+" Essayez de trouver le nombre")
        information = input("(" + set_color_green(currentPlayers.player1.name)+ ")"+ " Entrez (trop petit), (trop grand) ou (c'est gagné) en fonction du nombre entree")
        while guess_number(gameRiddle,information,int(choice)):
            information = input("(" + set_color_green(currentPlayers.player1.name)+ ")"+" ne mentez pas! Entrez (trop petit), (trop grand) ou (c'est gagné) en fonction du nombre entree")
        if int(choice) == gameRiddle.numberToGuess:
            winner = currentPlayers.player2
            gameRiddle.isOver = True
        elif gameRiddle.attempts >= gameRiddle.maxAttempts:
            winner = currentPlayers.player1
            gameRiddle.isOver = True

    looser = getOtherPlayer(currentPlayers,winner)
    display_result(gameRiddle, looser, winner)
    pointsDistribution(gameRiddle,winner,looser,conn)
     

"""
#data set de test tout ca est fait dans le main normalement
cp : CurrentPlayers
p1 :Player
p2: Player
p1 = Player()
p2 = Player()

p1.id = 1
p1.name = "Louis"
p1.scoreMatches = 10
p1.scoreP4 = 10
p1.scoreRiddle = 10
p1.scoreTtt  = 10

p2.id = 10
p2.name = "Lorie"
p2.scoreMatches = 10
p2.scoreP4 = 10
p2.scoreRiddle = 10
p2.scoreTtt  = 10
cp = CurrentPlayers()
cp.player1 = p1
cp.player2 = p2
currentPlayersInit(cp,p1,p2)
#game(cp)

con = sqlite3.connect("db.sqlite")
game(cp,con)
"""