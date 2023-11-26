from colors import *
def displayStartingMenu(gameName:  str, rules: list[str])->None:
    """
        Affiche le menu de démarrage du jeu Puissance 4.

        Cette fonction affiche le menu de démarrage du jeu Puissance 4, y compris un message de bienvenue, les règles du jeu et un message de chargement.

        Args:
            None

        Returns:
            None

    """
    i : int

    print(setColorGreen(f"Bienvenue à vous dans le jeu du {gameName}"))
    for i in range(0,len(rules)) :
        print(setColorGreen(rules[i]))
