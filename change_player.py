from player import CurrentPlayers,Player

def change_player(currPlayers: CurrentPlayers):
    """
        Permet d'echanger le joueur1 avec le joueur2 pour que le role change en fonction du jeu

        Args :
            currPlayers (CurrPlayers) cette variable represente les deux joueur qui jouent actuellement
        Return:
            Rien
    """
    tmp : Player

    tmp = currPlayers.player1
    currPlayers.player1 = currPlayers.player2
    currPlayers.player2 = tmp

