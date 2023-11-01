from player import CurrentPlayers,Player

def changePlayer(currPlayers: CurrentPlayers):
    """
        Permet d'echanger le joueur1 avec le joueur2 pour que le role change en fonction du jeu

        Args :
            currPlayers (CurrPlayers) cette variable represente les deux joueur qui jouent actuellement
        Return:
            Rien
    """
    tmpPlayer : Player
    tmpValue : int

    #Changer les joueurs
    tmpPlayer = currPlayers.player1
    currPlayers.player1 = currPlayers.player2
    currPlayers.player2 = tmpPlayer
    #Changer valeurs
    tmpValue = currPlayers.player1.playerNumber
    currPlayers.player1.playerNumber = currPlayers.player2.playerNumber
    currPlayers.player2.playerNumber = tmpValue

def getOtherPlayer(currentPlayers: CurrentPlayers, currentPlayer : Player)->Player:
    if currentPlayer == currentPlayers.player1:
        return currentPlayers.player2
    return currentPlayers.player1