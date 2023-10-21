import sqlite3
from player import CurrentPlayers,Player,currentPlayersInit
from sql_commands import connect,register
from colors import *
currentPlayers : CurrentPlayers
player1 : Player
player2 : Player

player1 = Player()
player2 = Player()

#l'id à -1 indique que le joueur n'est pas connecté
player1.id = -1
player2.id = -1
currentPlayers = CurrentPlayers()

con = sqlite3.connect("db.sqlite")
cur = con.cursor()
print(set_color_green("Bienvenue à vous! etes vous prets à jouer?"))
print(set_color_green("Chargement..."))
print(set_color_yellow("Je vois que vous n'etes pas connectés"))


while player1.id == -1:
    print("Connectez-vous à votre compte joueur 1")
    choice = int(input("vous souhaiter vous "+ set_color_green("connecter(0)") + " ou vous "+ set_color_green("inscrire(1)")))
    username = input("username")
    password = input("password")
    if choice == 0:
        player1 = connect(username,password, cur)
        if player1.id == -1:
            print(set_color_red("Mot de passe ou nom d'utilisateur invalide"))
    else:
        pass
   
while player2.id == -1:
    print("Connectez-vous à votre compte joueur 2")
    choice = int(input("vous souhaiter vous "+ set_color_green("connecter(0)") + " ou vous "+ set_color_green("inscrire(1)")))
    username = input("username")
    password = input("password")
    if choice == 0 :
        player2 = connect(username,password, cur)
        if player2.id == -1:
            print(set_color_red("Mot de passe ou nom d'utilisateur invalide"))
        elif player1.id == player2.id:
            print(set_color_red("⚠️ Ce joueur est déjà connecté"))
            player2.id = -1
    else:
        pass

currentPlayersInit(currentPlayers, player1, player2)
end = False
while not end:
    print(set_color_green("YAA! choisi ton jeu:\n"))
    gameChoice = int(input("1 => jeu des devinettes \n2 => jeu des allumettes\n3 => jeu du morpion"))

    match gameChoice:
        case 1:
            print("jeu")
        case 5:
            print("quitter")
            end = True
        case _:
            print(set_color_red("ce choix n'existe pas"))
