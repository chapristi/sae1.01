from helpers.colors import *
def displayStartingMenu(gameName: str, rules: list[str]) -> None:
    """
    Affiche le menu de démarrage du jeu.

    Args:
        gameName (str): Nom du jeu à afficher dans le message de bienvenue.
        rules (list[str]): Liste des règles du jeu à afficher.

    Returns:
        None
    """
    # Variable de boucle
    i: int

    # Affiche le message de bienvenue avec le nom du jeu en vert
    print(setColorGreen(f"Bienvenue à vous dans le jeu du {gameName}"))

    # Affiche chaque règle du jeu en vert
    for i in range(0, len(rules)):
        print(setColorGreen(rules[i]))
    print()
