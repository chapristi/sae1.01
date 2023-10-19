#from player import CurrentPlayers
from game_match import GameMatch, gameMatchInit
from colors import set_color_green,set_color_red,set_color_yellow
from input_checker import isDigit
def display_win() -> None:
    print(set_color_green("bravo le joueur x a gagner 100 points en revanche le joueur y gagne 0 points "))

def display_starting_menu() -> None:
    print(set_color_yellow("Bienvenue sur le jeu des Allumettes etes vous pret a jouer?"))
    print("chargement...")
   
def draw_matches(nb : int) -> None:
    matches : list[str]
    i: int

    i = 0
    matches = [
         set_color_red("█"),
         set_color_yellow ("█"),
         set_color_yellow ("█"),
         set_color_yellow ("█"),
         set_color_yellow ("█"),
    ]
    for i in range(0,5):
        print()
        for _ in range(0,nb):
            print(matches[i] + " ",end="")
    print()

def game() -> None:
    """
        currentPLayers : CurrentPlayers
    """
    gameMatch : GameMatch
    curr_player : bool
    choice  : str

    curr_player = True
    gameMatch = GameMatch()
    gameMatchInit(gameMatch)
    display_starting_menu()

    while gameMatch.numberOfMatches > 0:
        draw_matches(gameMatch.numberOfMatches)
        print(curr_player, "a vous de jouer")
        choice = input("choisissez entre 1,2,3 allumettes a retirer ")
        
        while not isDigit(choice) or int(choice) < 1 or int(choice) > 3:
            choice = input("choisissez entre 1,2,3 allumettes a retirer ")
        gameMatch.numberOfMatches -= int(choice)
        if gameMatch.numberOfMatches > 0:
            curr_player = not curr_player

    display_win()
        
        

    

game()  


