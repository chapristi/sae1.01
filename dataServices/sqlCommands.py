from sqlite3 import Connection,Cursor
from entity.player import Player,playerInit

def register(name : str, password : str, conn : Connection)->Player:
    """
        Enregistre un nouveau joueur dans la base de données avec un nom et un mot de passe.

        Cette fonction permet d'enregistrer un nouveau joueur en fournissant son nom et son mot de passe. Le joueur est ajouté à la base de données avec des scores initiaux nuls pour chaque jeu.

        Args:
            name (str): Le nom du joueur.
            password (str): Le mot de passe du joueur.
            conn (Connection): La connexion à la base de données.

        Returns:
            Player: L'objet Player du joueur nouvellement enregistré avec son identifiant et ses scores initiaux.
                En cas d'erreur, un objet Player avec un identifiant de -1 est renvoyé pour indiquer un échec.

    """
    res : Cursor 
    cur: Cursor | None
    query : str
    playerElements : list[str] | None

    player : Player
    player = Player()
    player.id = -1
    cur  = None

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
    except Exception:
        player.id = -1
        return player
    finally:
        if cur is not None:
            cur.close()




def connect(name :str, password : str , conn : Connection) -> Player:
    """
        Connecte un joueur en vérifiant le nom d'utilisateur et le mot de passe dans la base de données.

        Cette fonction permet à un joueur de se connecter en vérifiant son nom d'utilisateur et son mot de passe dans la base de données. Si les informations d'identification sont correctes, le joueur est chargé avec ses scores depuis la base de données.

        Args:
            name (str): Le nom d'utilisateur du joueur.
            password (str): Le mot de passe du joueur.
            conn (Connection): La connexion à la base de données.

        Returns:
            Player: L'objet Player du joueur connecté avec son identifiant et ses scores.
                En cas d'informations d'identification incorrectes ou d'erreur, un objet Player avec un identifiant de -1 est renvoyé.

    """
    res : Cursor
    query : str
    cur: Cursor | None
    playerElements : list[str] | None
    player : Player
    player = Player()
    player.id = -1
    cur = None

    try :
        cur = conn.cursor()
        query = f"SELECT id,name,scoreRiddle,scoreTtt,scoreMatches, scoreP4 FROM PLAYER WHERE name = ? AND password = ?"
        res = cur.execute(
                    query,(
                        name,
                        password
                    ))
        playerElements  = res.fetchone()
        if playerElements == None:
            return player
        playerInit(player, int(playerElements[0]), playerElements[1],int(playerElements[2]), int(playerElements[3]), int(playerElements[4]),int(playerElements[5]))
        return player
    except Exception:
        return player
    finally:
        if cur is not None:
            cur.close()
    
    



def addPoint(id : int, points: int, conn : Connection, game : str)->bool:
    """
        Ajoute des points au score d'un joueur dans un jeu spécifié.

        Cette fonction permet d'ajouter un certain nombre de points au score d'un joueur dans un jeu spécifié. Le joueur est identifié par son ID dans la base de données.

        Args:
            id (int): L'identifiant du joueur auquel ajouter des points.
            points (int): Le nombre de points à ajouter au score du joueur.
            conn (Connection): La connexion à la base de données.
            game (str): Le nom du jeu pour lequel les points sont ajoutés.

        Returns:
            bool: True si l'ajout de points s'est déroulé avec succès, False en cas d'erreur.

    """
    cur : Cursor | None
    query : str
    cur  = None
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
        return False
    finally:
        if cur is not None:
            cur.close()
    
def getTopUsersByColumn(collName: str ,conn : Connection) -> list[list[str]]:
    """
        Récupère les meilleurs joueurs triés par score dans une colonne spécifiée de la base de données.

        Cette fonction interroge la base de données pour récupérer les 10 meilleurs joueurs classés par score dans une colonne spécifiée.

        Args:
            collName (str): Le nom de la colonne pour laquelle récupérer les meilleurs joueurs.
            conn (Connection): La connexion à la base de données.

        Returns:
            list[list[str]]: Une liste de listes contenant les informations des meilleurs joueurs, y compris leur ID, nom et score dans la colonne spécifiée.
                            En cas d'erreur, une liste vide est renvoyée.

    """
    res : Cursor 
    cur: Cursor | None
    query : str
    playersElements : list[list[str]]
    playersElements = list(list())
    cur = None
    try:
        cur = conn.cursor()
        query = f"SELECT id,name, {collName} as score FROM PLAYER ORDER BY score DESC LIMIT 10;"
        res = cur.execute(
                    query,(     
                    ))
        playersElements  = res.fetchall()
        return playersElements
    except Exception:
        return playersElements
    finally:
        if cur is not None:
            cur.close()


