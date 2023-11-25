from dataServices.sqlCommands import getTopUsersByColumn
from sqlite3 import Connection
from helpers.colors import setColorYellow
def leaderBoardN(name: str, collName:str, conn : Connection)->None:
    """
        Affiche le tableau du Leaderboard pour une colonne donnée.

        Cette fonction affiche le tableau du Leaderboard pour une colonne spécifiée (nommée `name`). Le Leaderboard est extrait de la collection `collName` de la base de données `conn`.

        Args:
            name (str): Le nom de la colonne pour laquelle afficher le Leaderboard.
            collName (str): Le nom de la collection dans la base de données contenant les données du Leaderboard.
            conn (Connection): L'objet de connexion à la base de données.

        Returns:
            None
    """

    users : list[list[str]]
    space : str

    space = " "
    users = getTopUsersByColumn(collName,conn)
    print(setColorYellow("Table du Leaderboard "+name +":\n"))
    print("ID    Nom            Score")
    print("-" * 30)
    for player in users:
        print(f"{player[0]}{space * (5 - len(str(player[0])))} "
                f"{player[1]}{space * (15 - len(str(player[1])))} "
                f"{player[2]}{space * (10 - len(str(player[2])))}")

    print()


def displayLeaderBoards(conn : Connection)->None:
    """
        Affiche les tableaux du Leaderboard pour plusieurs colonnes.

        Cette fonction affiche les tableaux du Leaderboard pour plusieurs colonnes spécifiées dans la liste `collName`, avec les noms correspondants dans la liste `names`. Les Leaderboards sont extraits de la base de données `conn`.

        Args:
            conn (Connection): L'objet de connexion à la base de données.

        Returns:
            None
    """
    collName : list[str]
    names : list[str]
    i : int

    collName = ["scoreTtt", "scoreMatches","scoreRiddle","scoreP4"]
    names = ["Tic Tac Toe" , "Allumettes", "Devinette", "Puissance 4"]
    i = 0

    for i in range(0,len(collName)):
        leaderBoardN(names[i],collName[i],conn)