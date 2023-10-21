from sqlite3 import Cursor
from player import Player,playerInit
def register(name : str, password : str, cur : Cursor)->list[str]:
    res : Cursor 
    res = cur.execute("INSERT INTO PLAYER (name,password,scoreRiddle,scoreTtt,scoreMatches,scoreP4) VALUES (?,?,0,0,0,0)",(name,password))
    if len(res.fetchone()) == 0:
        return [""]
    return res.fetchone()

def connect(name :str, password : str , cur : Cursor) -> Player:
    res : Cursor
    req : str
    playerElements : list[str] | None
    player : Player
    player = Player()

    req = "SELECT id,name,scoreRiddle,scoreTtt,scoreMatches, scoreP4 FROM PLAYER WHERE name ='" + name + "' AND password = '"+ password + "'"
    res = cur.execute(req)
    playerElements  = res.fetchone()
    if playerElements == None:
        player.id = -1
        return player
    playerInit(player, int(playerElements[0]), playerElements[1],int(playerElements[2]), int(playerElements[3]), int(playerElements[4]),int(playerElements[5]))
    return player

