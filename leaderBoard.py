from sql_commands import getTopUsersByColumn
from sqlite3 import Connection
def leaderBoardN(name: str,collName:str, conn : Connection):
    users : list[list[str | int]]
    users = getTopUsersByColumn(collName,conn)
    print("Table du Leaderboard "+name +":\n")
    print("ID    Nom            Score")
    print("-" * 30)
    for player in users:
        print(f"{player[0]:<5} {player[1]:<15} {player[2]:<10}")
    print("\n")


def displayLeaderBoards(conn : Connection):
    collName : list[str]
    names : list[str]
    i : int

    collName = ["scoreTtt", "scoreMatches","scoreRiddle","scoreP4"]
    names= ["Tic Tac Toe" , "Allumettes", "Devinette", "Puissance 4"]
    i = 0

    for i in range(0,len(collName)):
        leaderBoardN(names[i],collName[i],conn)