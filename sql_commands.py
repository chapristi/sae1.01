from sqlite3 import Connection,Cursor
import sqlite3
from player import Player,playerInit
def register(name : str, password : str, conn : Connection)->Player:
    res : Cursor 
    cur: Cursor
    query : str
    playerElements : list[str] | None

    player : Player
    player = Player()
    player.id = -1

    try:
        cur = conn.cursor()
        query = f"INSERT INTO PLAYER (name,password,scoreRiddle,scoreTtt,scoreMatches,scoreP4) VALUES (?,?,0,0,0,0)"
        cur.execute(query,(name,password))
        conn.commit()
        query = f"SELECT id,name,scoreRiddle,scoreTtt,scoreMatches,scoreP4 FROM PLAYER WHERE id = ?"
        res = cur.execute(
                    query,(
                        str(cur.lastrowid),
                ))
        playerElements  = res.fetchone()
        if playerElements == None:
            return player
        playerInit(player, int(playerElements[0]), playerElements[1],int(playerElements[2]), int(playerElements[3]), int(playerElements[4]),int(playerElements[5]))
        return player
    except sqlite3.IntegrityError:
        return player


def connect(name :str, password : str , conn : Connection) -> Player:
    res : Cursor
    query : str
    cur: Cursor
    playerElements : list[str] | None
    player : Player
    player = Player()

    cur = conn.cursor()
    query = f"SELECT id,name,scoreRiddle,scoreTtt,scoreMatches, scoreP4 FROM PLAYER WHERE name = ? AND password = ?"
    res = cur.execute(
                query,(
                    name,
                    password
                ))
    playerElements  = res.fetchone()
    if playerElements == None:
        player.id = -1
        return player
    playerInit(player, int(playerElements[0]), playerElements[1],int(playerElements[2]), int(playerElements[3]), int(playerElements[4]),int(playerElements[5]))
    return player

def addPoint(id : int, points: int, conn : Connection, game : str)->bool:
    """
        id permet d'identifier la personne qui va remporter des points
        points c'est le nombre de points remportés
    """
    try:
        cur = conn.cursor()
        query = f"UPDATE PLAYER SET {game} = {game} + ? WHERE id = ?;"
        cur.execute(
            query, (
                points,
                id
            )
        )
        conn.commit()
        return True
    except Exception:
        #print(error)
        return False
    
def getTopUsersByColumn(collName: str ,conn : Connection) -> list[list[str | int]]:
    res : Cursor 
    cur: Cursor
    query : str
    playersElements : list[list[str | int]]

    cur = conn.cursor()
    query = f"SELECT id,name, {collName} as score FROM PLAYER ORDER BY score DESC LIMIT 10;"
    res = cur.execute(
                query,(
                       
                ))
    playersElements  = res.fetchall()
    return playersElements


