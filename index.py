import sqlite3
from entity.player import CurrentPlayers,Player,currentPlayersInit
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

    con = sqlite3.connect("db.sqlite")

    print(setColorGreen("Bienvenue à vous! etes vous prets à jouer?"))
    print(setColorGreen("Chargement..."))
    print(setColorYellow("Je vois que vous n'etes pas connectés"))

    while player1.id == -1:
        print("Connectez-vous à votre compte joueur 1")
        choice = input("vous souhaiter vous "+ setColorGreen("connecter(0)") + " ou vous "+ setColorGreen("inscrire(1)"))
        while not isDigit(choice) or (int(choice) != 0 and int(choice) != 1):
            choice = input(setColorYellow("vous souhaiter vous "+ setColorGreen("connecter(0)") + " ou vous "+ setColorGreen("inscrire(1)")))
        username = input("username")
        password = getpass.getpass("password")
        if int(choice) == 0:
            player1 = connect(username,password, con)
            if player1.id == -1:
                print(setColorRed("Mot de passe ou nom d'utilisateur invalide"))
        elif int(choice) == 1:
            player1 = register(username,password,con)
            if player1.id == -1:
                print(setColorRed("⚠️ Ce nom d'utilisateur est déjà utilisé"))
        else:
            print(setColorRed("ce choix n'existe pas"))

    while player2.id == -1:
        print("Connectez-vous à votre compte joueur 2")
        choice = input("vous souhaiter vous "+ setColorGreen("connecter(0)") + " ou vous "+ setColorGreen("inscrire(1)"))
        while not isDigit(choice) or (int(choice) != 0 and int(choice) != 1):
            choice = input(setColorYellow("vous souhaiter vous "+ setColorGreen("connecter(0)") + " ou vous "+ setColorGreen("inscrire(1)")))
        username = input("username")
        password = getpass.getpass("password")
        if int(choice) == 0 :
            player2 = connect(username,password, con)
            if player2.id == -1:
                print(setColorRed("Mot de passe ou nom d'utilisateur invalide"))
            elif player1.id == player2.id:
                print(setColorRed("⚠️ Ce joueur est déjà connecté"))
                player2.id = -1
        elif int(choice) == 1:
            player2 = register(username,password,con)
            if player2.id == -1:
                print(setColorRed("⚠️ Ce nom d'utilisateur est déjà utilisé"))

        else:
            print(setColorRed("ce choix n'existe pas"))
            
    currentPlayersInit(currentPlayers, player1, player2)
    end = False
    while not end:
        print(setColorGreen("\nYAA! choisisez le jeu:\n"))
        gameChoice = input("1 => jeu des devinettes \n2 => jeu des allumettes\n3 => jeu du morpion\n4 => jeu du puissance 4\n5 => Classement\n6 => quitter\nmon choix est  ")
        while not isDigit(gameChoice):
            print(setColorRed("ce choix n'existe pas\n"))
            gameChoice = input("1 => jeu des devinettes \n2 => jeu des allumettes\n3 => jeu du morpion\n4 => jeu du puissance 4\n5 => Classement\n6 => quitter\nmon choix est  ")

        match int(gameChoice):
            case 1 : 
                gameRiddle(currentPlayers,con)
            case 4:
                gameP4(currentPlayers,con)
            case 3:
                gameTicTacToe(currentPlayers,con)
            case 2:
                gameMatch(currentPlayers,con)
            case 5: 
                displayLeaderBoards(con)
            case 6:
                print(setColorGreen("Merci d'avoir joué à bientot"))
                end = True
            case _:
                print(setColorRed("ce choix n'existe pas"))
        changePlayer(currentPlayers)
    con.close()