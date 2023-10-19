# Codes ANSI pour les couleurs
red = "\u001b[31;1m"
yellow = "\u001b[33m"

def draw_alum(nb : int) -> None:
    matches : list[str]
    i: int

    i = 0
    matches = [
         red + "█",
         yellow + "█",
         yellow + "█",
         yellow + "█",
         yellow + "█"
    ]
    for i in range(0,5):
        print()
        for _ in range(0,nb):
            print(matches[i] + " ",end="")

draw_alum(5)