class Player:
    id : int
    name : str
    playerNumber : int
    

def playerInit(player : Player,id : int,name : str)->None:
    """
        Initialise un objet joueur avec les informations fournies.

        Cette fonction initialise un objet joueur avec un identifiant, un nom et les scores pour différents jeux.

        Args:
            player (Player): L'objet de joueur à initialiser.
            id (int): L'identifiant du joueur.
            name (str): Le nom du joueur.
            scoreRiddle (int): Le score du joueur dans le jeu de Devinette.
            scoreTtt (int): Le score du joueur dans le jeu de Tic Tac Toe.
            scoreMatches (int): Le score du joueur dans le jeu des Allumettes.
            scoreP4 (int): Le score du joueur dans le jeu de Puissance 4.

        Returns:
            None
    """
    player.id = id
    player.name = name
   

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
