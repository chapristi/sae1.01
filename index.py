import sqlite3
from entity.player import * 
from helpers.helperPlayer import changePlayer
from dataServices.sqlCommands import connect,register
from helpers.colors import *
from helpers.inputChecker import isDigit
from match import game as gameMatch
from p4 import game as gameP4
from riddle import game as gameRiddle
from leaderBoard import displayLeaderBoards
from ticTacToe import game as gameTicTacToe
import getpass


if __name__ == "__main__":
    currentPlayers : CurrentPlayers
    player1 : Player
    player2 : Player
    choice: str
    username : str
    password : str
    con : sqlite3.Connection

    player1 = Player()
    player2 = Player()

    #l'id à -1 indique que le joueur n'est pas connecté
    player1.id = -1
    player2.id = -1
    currentPlayers = CurrentPlayers()
    #connexion à la base de données
    con = sqlite3.connect("db.sqlite")

    print(setColorGreen("Bienvenue à vous! etes vous prets à jouer?"))
    print(setColorGreen("Chargement..."))
    print(setColorYellow("Je vois que vous n'etes pas connectés"))

    while player1.id == -1:
        print("Connectez-vous à votre compte joueur 1")
        choice = input("Vous souhaiter vous "+ setColorGreen("connecter(0)") + " , vous "+ setColorGreen("inscrire(1)") + " ou "+ setColorGreen("bot(2)"))
        while not isDigit(choice) or (int(choice) != 0 and int(choice) != 1 and int(choice) != 2):
            choice = input(setColorYellow("Vous souhaiter vous "+ setColorGreen("connecter(0)") + " , vous "+ setColorGreen("inscrire(1)") + " ou "+ setColorGreen("bot(2)")))
        if int(choice) == 0:
            username = input("nom d'utilisateur ")
            password = getpass.getpass("mot de passe ")
            player1 = connect(username,password, con)
            player1.isBot = False
            if player1.id == -1:
                print(setColorRed("Mot de passe ou nom d'utilisateur invalide"))
        elif int(choice) == 1:
            username = input("nom d'utilisateur ")
            password = getpass.getpass("mot de passe ")
            player1 = register(username,password,con)
            if player1.id == -1:
                print(setColorRed("⚠️ Ce nom d'utilisateur est déjà utilisé"))
        elif int(choice) == 2:
            botLvl = input("Entrez le niveau du bot (1 à 5)")
            while not isDigit(botLvl) or not (1 <= int(botLvl) <= 5):
                botLvl = input(setColorYellow("⚠️ entrez le niveau du bot de 1 à 5"))
            playerInit(player1,2,"Bot LaLa",True,int(botLvl))
        else:
            print(setColorRed("Ce choix n'existe pas"))

    while player2.id == -1:
        print("Connectez-vous à votre compte joueur 2")
        choice = input("vous souhaiter vous "+ setColorGreen("connecter(0)") + ", vous "+ setColorGreen("inscrire(1)") + " ou "+ setColorGreen("bot(2)"))
        while not isDigit(choice) or (int(choice) != 0 and int(choice) != 1 and int(choice) != 2 ):
            choice = input(setColorYellow("Vous souhaiter vous "+ setColorGreen("connecter(0)") + " , vous "+ setColorGreen("inscrire(1)") + " ou "+ setColorGreen("bot(2)")))
        if int(choice) == 0 :
            username = input("nom d'utilisateur ")
            password = getpass.getpass("mot de passe ")
            player2 = connect(username,password, con)
            if player2.id == -1:
                print(setColorRed("Mot de passe ou nom d'utilisateur invalide"))
            elif player1.id == player2.id:
                print(setColorRed("⚠️ Ce joueur est déjà connecté"))
                player2.id = -1
        elif int(choice) == 1:
            username = input("nom d'utilisateur ")
            password = getpass.getpass("mot de passe ")
            player2 = register(username,password,con)
            if player2.id == -1:
                print(setColorRed("⚠️ Ce nom d'utilisateur est déjà utilisé"))
        elif int(choice) == 2:
            botLvl = input("Entrez le niveau du bot (1 à 5)")
            while not isDigit(botLvl) or not (1 <= int(botLvl) <= 5):
                botLvl = input(setColorYellow("⚠️ entrez le niveau du bot de 1 à 5"))
            playerInit(player2,1,"Bot Patoche",True,int(botLvl))
        else:
            print(setColorRed("Ce choix n'existe pas"))
    # Initialisation des joueurs qui s'apprêtent à jouer        
    currentPlayersInit(currentPlayers, player1, player2)
    end = False
    while not end:
        print(setColorGreen("\nChoisisez le jeu:\n"))
        gameChoice = input("1 => Pour jouer aux devinettes \n2 => Pour jouer au jeu des allumettes\n3 => Pour jouer au jeu du morpion\n4 => Pour jouer au jeu du puissance 4\n5 => Pour afficher le classement des joueurs par jeux\n6 => Pour quitter le jeu\nMon choix est  ")
        while not isDigit(gameChoice):
            print(setColorRed("Ce choix n'existe pas\n"))
            gameChoice = input("1 => Pour jouer aux devinettes \n2 => Pour jouer au jeu des allumettes\n3 => Pour jouer au jeu du morpion\n4 => Pour jouer au jeu du puissance 4\n5 => Pour afficher le classement des joueurs par jeux\n6 => Pour quitter le jeu\nMon choix est  ")
        if int(gameChoice) ==  1: 
            gameRiddle(currentPlayers,con)
        elif int(gameChoice) ==   4:
            gameP4(currentPlayers,con)
        elif  int(gameChoice) ==  3:
            gameTicTacToe(currentPlayers,con)
        elif int(gameChoice) == 2:
            gameMatch(currentPlayers,con)
        elif int(gameChoice) ==  5: 
            displayLeaderBoards(con)
        elif int(gameChoice) ==  6:
            print(setColorGreen("Merci d'avoir joué à bientot"))
            end = True
        else:
            print(setColorRed("Ce choix n'existe pas"))
        changePlayer(currentPlayers)
    #fermeture de la connection à la base de données.
    con.close()